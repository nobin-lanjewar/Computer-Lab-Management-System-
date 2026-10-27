from datetime import date, time, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.labs.models import Computer, Lab, MaintenanceRecord
from apps.schedules.models import LabSchedule
from apps.students.models import Student


class ManagementPageSmokeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin", email="admin@example.test", password="safe-password"
        )
        self.client.force_login(self.user)
        self.lab = Lab.objects.create(
            name="Main Lab", room_number="A-101", capacity=20
        )
        self.computer = Computer.objects.create(
            lab=self.lab, computer_number="PC-01", computer_name="Workstation 1"
        )
        self.student = Student.objects.create(
            student_id="ST-001",
            name="Asha Patil",
            class_department="Computing",
            email="asha@example.test",
        )
        self.schedule = LabSchedule.objects.create(
            lab=self.lab,
            computer=self.computer,
            student=self.student,
            date=date.today() + timedelta(days=1),
            start_time=time(9, 0),
            end_time=time(10, 0),
            purpose="Practice",
            requester=self.user,
        )
        self.maintenance = MaintenanceRecord.objects.create(
            computer=self.computer, issue="Intermittent restart"
        )

    def test_lists_forms_and_confirmation_pages_render(self):
        pages = [
            "dashboard:index",
            "labs:lab-list",
            "labs:lab-create",
            "labs:lab-update",
            "labs:lab-delete",
            "labs:computer-list",
            "labs:computer-create",
            "labs:computer-update",
            "labs:computer-delete",
            "labs:maintenance-list",
            "labs:maintenance-create",
            "labs:maintenance-update",
            "labs:maintenance-delete",
            "students:student-list",
            "students:student-create",
            "students:student-update",
            "students:student-delete",
            "schedules:schedule-list",
            "schedules:schedule-create",
            "schedules:schedule-update",
            "schedules:schedule-delete",
        ]
        objects = {
            "labs:lab-update": self.lab.pk,
            "labs:lab-delete": self.lab.pk,
            "labs:computer-update": self.computer.pk,
            "labs:computer-delete": self.computer.pk,
            "labs:maintenance-update": self.maintenance.pk,
            "labs:maintenance-delete": self.maintenance.pk,
            "students:student-update": self.student.pk,
            "students:student-delete": self.student.pk,
            "schedules:schedule-update": self.schedule.pk,
            "schedules:schedule-delete": self.schedule.pk,
        }

        for page in pages:
            with self.subTest(page=page):
                args = [objects[page]] if page in objects else []
                response = self.client.get(reverse(page, args=args))
                self.assertEqual(response.status_code, 200)
