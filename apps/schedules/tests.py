from datetime import date, time

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.labs.models import Computer, Lab
from apps.students.models import Student

from .models import LabSchedule


class LabScheduleModelTests(TestCase):
    def setUp(self):
        self.lab = Lab.objects.create(name="Computer Lab", room_number="R-201")
        self.computer = Computer.objects.create(
            lab=self.lab, computer_number="PC-01"
        )
        self.student = Student.objects.create(
            student_id="ST-101", name="Meera Shah", class_department="Computer"
        )

    def make_schedule(self, **overrides):
        values = {
            "lab": self.lab,
            "computer": self.computer,
            "student": self.student,
            "date": date(2026, 10, 27),
            "start_time": time(9, 0),
            "end_time": time(10, 0),
            "purpose": "Programming practice",
        }
        values.update(overrides)
        return LabSchedule(**values)

    def test_rejects_schedule_without_student_or_class(self):
        schedule = self.make_schedule(student=None)

        with self.assertRaises(ValidationError):
            schedule.full_clean()

    def test_rejects_computer_from_another_lab(self):
        other_lab = Lab.objects.create(name="Physics Lab", room_number="R-202")
        other_computer = Computer.objects.create(
            lab=other_lab, computer_number="PC-01"
        )
        schedule = self.make_schedule(computer=other_computer)

        with self.assertRaises(ValidationError):
            schedule.full_clean()

    def test_rejects_overlapping_booking_for_same_computer(self):
        self.make_schedule().save()
        overlapping = self.make_schedule(
            start_time=time(9, 30), end_time=time(10, 30)
        )

        with self.assertRaises(ValidationError):
            overlapping.full_clean()

    def test_lab_wide_booking_conflicts_with_computer_booking(self):
        self.make_schedule().save()
        lab_wide_booking = self.make_schedule(
            computer=None,
            student=None,
            class_name="Diploma Computer Technology",
            start_time=time(9, 30),
            end_time=time(10, 30),
        )

        with self.assertRaises(ValidationError):
            lab_wide_booking.full_clean()

    def test_computer_booking_conflicts_with_existing_lab_wide_booking(self):
        self.make_schedule(
            computer=None,
            student=None,
            class_name="Diploma Computer Technology",
        ).save()
        computer_booking = self.make_schedule(
            start_time=time(9, 30), end_time=time(10, 30)
        )

        with self.assertRaises(ValidationError):
            computer_booking.full_clean()

    def test_allows_non_overlapping_booking_for_same_computer(self):
        self.make_schedule().save()
        later_booking = self.make_schedule(
            start_time=time(10, 0), end_time=time(11, 0)
        )

        later_booking.full_clean()
