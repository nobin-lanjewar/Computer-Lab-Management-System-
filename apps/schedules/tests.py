from datetime import date, time

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import Permission, User
from django.urls import reverse

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

    def test_rejects_end_time_not_later_than_start_time_on_save(self):
        invalid = self.make_schedule(start_time=time(10, 0), end_time=time(10, 0))

        with self.assertRaises(ValidationError):
            invalid.save()

    def test_cancelled_booking_does_not_block_a_new_booking(self):
        cancelled = self.make_schedule(status=LabSchedule.Status.CANCELLED)
        cancelled.save()

        self.make_schedule().save()
        self.assertEqual(LabSchedule.objects.count(), 2)

    def test_computer_under_maintenance_cannot_be_booked(self):
        self.computer.status = Computer.Status.UNDER_MAINTENANCE
        self.computer.save()
        schedule = self.make_schedule()

        with self.assertRaises(ValidationError):
            schedule.full_clean()

    def test_inactive_lab_cannot_be_booked(self):
        self.lab.is_active = False
        self.lab.save()

        with self.assertRaises(ValidationError):
            self.make_schedule().full_clean()

    def test_booking_creation_requires_permission_and_records_requester(self):
        anonymous_response = self.client.get(reverse("schedules:schedule-create"))
        self.assertEqual(anonymous_response.status_code, 302)

        user = User.objects.create_user(username="student-user", password="safe-password")
        permission = Permission.objects.get(
            content_type__app_label="schedules", codename="add_labschedule"
        )
        user.user_permissions.add(permission)
        self.client.force_login(user)
        response = self.client.post(
            reverse("schedules:schedule-create"),
            {
                "lab": self.lab.pk,
                "computer": "",
                "class_name": "Computer Department",
                "date": "2026-10-28",
                "start_time": "09:00",
                "end_time": "10:00",
                "purpose": "Programming practice",
            },
        )

        self.assertRedirects(response, reverse("dashboard:index"))
        schedule = LabSchedule.objects.get(date=date(2026, 10, 28))
        self.assertEqual(schedule.requester, user)
        self.assertEqual(schedule.status, LabSchedule.Status.REQUESTED)

    def test_booking_list_limits_students_to_their_own_records(self):
        viewer = User.objects.create_user(username="booking-viewer", password="safe-password")
        other_user = User.objects.create_user(username="other", password="safe-password")
        viewer.user_permissions.add(
            Permission.objects.get(
                content_type__app_label="schedules",
                codename="view_labschedule",
            )
        )
        self.make_schedule(
            purpose="My private booking",
            date=date(2026, 10, 28),
            requester=viewer,
        ).save()
        self.make_schedule(
            purpose="Other private booking",
            date=date(2026, 10, 29),
            requester=other_user,
        ).save()
        self.client.force_login(viewer)

        response = self.client.get(reverse("schedules:schedule-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My private booking")
        self.assertNotContains(response, "Other private booking")
