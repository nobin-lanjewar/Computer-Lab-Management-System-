from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from apps.common.auth import (
    LAB_ASSISTANT_ROLE,
    STUDENT_ROLE,
    assign_role,
)
from apps.students.models import Student

from apps.labs.models import Computer, Lab, MaintenanceRecord
from apps.schedules.models import LabSchedule
from apps.students.models import Student


class DashboardViewTests(TestCase):
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard:index"))

        self.assertEqual(response.status_code, 302)

    def test_login_redirects_users_to_their_role_dashboard_and_logout_ends_session(self):
        user = User.objects.create_user(username="student-user", password="safe-password")
        Student.objects.create(
            user=user,
            student_id="ST-101",
            name="Asha Shah",
            class_department="Computing",
            email="asha@example.test",
        )
        assign_role(user, STUDENT_ROLE)

        response = self.client.post(
            reverse("login"),
            {"username": "student-user", "password": "safe-password"},
        )
        self.assertRedirects(response, reverse("dashboard:student"))
        self.assertEqual(
            self.client.get(reverse("dashboard:student")).status_code, 200
        )

        logout_response = self.client.post(reverse("logout"))
        self.assertRedirects(logout_response, reverse("login"))
        self.assertRedirects(
            self.client.get(reverse("dashboard:student")),
            f"{reverse('login')}?next={reverse('dashboard:student')}",
        )

    def test_role_dashboards_enforce_roles_server_side(self):
        student_user = User.objects.create_user(
            username="student-user", password="safe-password"
        )
        Student.objects.create(
            user=student_user,
            student_id="ST-102",
            name="Asha Shah",
            class_department="Computing",
            email="asha2@example.test",
        )
        assign_role(student_user, STUDENT_ROLE)
        self.client.force_login(student_user)

        self.assertEqual(
            self.client.get(reverse("dashboard:admin")).status_code, 403
        )
        self.client.logout()

        assistant = User.objects.create_user(
            username="assistant", password="safe-password"
        )
        assign_role(assistant, LAB_ASSISTANT_ROLE)
        self.client.force_login(assistant)
        self.assertEqual(
            self.client.get(reverse("dashboard:lab-assistant")).status_code, 200
        )
        self.assertEqual(
            self.client.get(reverse("dashboard:student")).status_code, 403
        )
        self.assertEqual(
            self.client.get(reverse("lab-assistant-create")).status_code, 403
        )

    def test_invalid_password_does_not_authenticate(self):
        User.objects.create_user(
            username="student-user", password="safe-password"
        )

        response = self.client.post(
            reverse("login"),
            {"username": "student-user", "password": "not-the-password"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)

    def test_only_admin_can_create_lab_assistant_accounts(self):
        response = self.client.get(reverse("lab-assistant-create"))
        self.assertEqual(response.status_code, 302)

        admin = User.objects.create_superuser(
            username="site-admin",
            email="admin@example.test",
            password="safe-password",
        )
        self.client.force_login(admin)
        response = self.client.post(
            reverse("lab-assistant-create"),
            {
                "username": "lab-assistant",
                "email": "assistant@example.test",
                "password1": "Strong-test-password-2026!",
                "password2": "Strong-test-password-2026!",
            },
        )

        self.assertRedirects(response, reverse("dashboard:admin"))
        assistant = User.objects.get(username="lab-assistant")
        self.assertFalse(assistant.is_staff)
        self.assertFalse(assistant.is_superuser)
        self.assertTrue(
            assistant.groups.filter(name=LAB_ASSISTANT_ROLE).exists()
        )
        self.assertTrue(assistant.has_perm("labs.add_lab"))
        self.assertTrue(assistant.check_password("Strong-test-password-2026!"))

    def test_login_redirects_admin_to_admin_dashboard(self):
        User.objects.create_superuser(
            username="site-admin",
            email="admin@example.test",
            password="safe-password",
        )
        response = self.client.post(
            reverse("login"),
            {"username": "site-admin", "password": "safe-password"},
        )

        self.assertRedirects(response, reverse("dashboard:admin"))

    def test_dashboard_displays_database_counts_and_upcoming_bookings(self):
        user = User.objects.create_user(username="viewer", password="safe-password")
        assign_role(user, LAB_ASSISTANT_ROLE)
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

        response = self.client.get(reverse("dashboard:lab-assistant"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["lab_count"], 1)
        self.assertEqual(response.context["computer_count"], 1)
        self.assertEqual(response.context["maintenance_computer_count"], 1)
        self.assertEqual(response.context["student_count"], 1)
        self.assertContains(response, schedule.purpose)
