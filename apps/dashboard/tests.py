from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from apps.labs.models import Computer, Lab, MaintenanceRecord
from apps.schedules.models import LabSchedule
from apps.students.models import Student


class DashboardViewTests(TestCase):
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard:index"))

        self.assertEqual(response.status_code, 302)

    def test_dashboard_displays_database_counts_and_upcoming_bookings(self):
        user = User.objects.create_user(username="viewer", password="safe-password")
        self.client.force_login(user)
        lab = Lab.objects.create(name="Main Lab", room_number="A-101", capacity=20)
        computer = Computer.objects.create(lab=lab, computer_number="PC-01")
        Student.objects.create(
            student_id="ST-101", name="Asha Shah", class_department="Computing"
        )
        schedule = LabSchedule.objects.create(
            lab=lab,
            computer=computer,
            class_name="Computing",
            requester=user,
            date="2026-11-01",
            start_time="09:00",
            end_time="10:00",
            purpose="Practice",
        )
        MaintenanceRecord.objects.create(computer=computer, issue="Intermittent restart")

        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["lab_count"], 1)
        self.assertEqual(response.context["computer_count"], 1)
        self.assertEqual(response.context["maintenance_computer_count"], 1)
        self.assertEqual(response.context["student_count"], 1)
        self.assertContains(response, schedule.purpose)
