from django.core.exceptions import ValidationError
from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from .forms import MaintenanceRecordForm
from .models import Computer, Lab, MaintenanceRecord


class LabAndComputerModelTests(TestCase):
    def setUp(self):
        self.lab = Lab.objects.create(name="Networking Lab", room_number="R-101")

    def test_computer_defaults_to_available(self):
        computer = Computer.objects.create(lab=self.lab, computer_number="PC-01")

        self.assertEqual(computer.status, Computer.Status.AVAILABLE)

    def test_computer_number_is_unique_within_a_lab(self):
        Computer.objects.create(lab=self.lab, computer_number="PC-01")
        duplicate = Computer(lab=self.lab, computer_number="PC-01")

        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_lab_capacity_must_be_positive(self):
        lab = Lab(name="Invalid Lab", room_number="R-102", capacity=0)

        with self.assertRaises(ValidationError):
            lab.full_clean()

    def test_maintenance_marks_computer_unavailable_and_resolution_restores_it(self):
        computer = Computer.objects.create(lab=self.lab, computer_number="PC-02")
        record = MaintenanceRecord.objects.create(computer=computer, issue="No display")

        computer.refresh_from_db()
        self.assertEqual(computer.status, Computer.Status.UNDER_MAINTENANCE)

        computer.status = Computer.Status.AVAILABLE
        computer.save()
        computer.refresh_from_db()
        self.assertEqual(computer.status, Computer.Status.UNDER_MAINTENANCE)

        record.status = MaintenanceRecord.Status.RESOLVED
        record.resolution = "Replaced display cable"
        record.save()
        computer.refresh_from_db()
        self.assertEqual(computer.status, Computer.Status.AVAILABLE)

    def test_resolved_maintenance_requires_resolution(self):
        computer = Computer.objects.create(lab=self.lab, computer_number="PC-03")
        record = MaintenanceRecord(
            computer=computer,
            issue="No display",
            status=MaintenanceRecord.Status.RESOLVED,
        )
        with self.assertRaises(ValidationError):
            record.save()

        form = MaintenanceRecordForm(
            data={
                "computer": computer.pk,
                "issue": "No display",
                "assigned_technician": "",
                "status": MaintenanceRecord.Status.RESOLVED,
                "resolution": "",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("resolution", form.errors)

    def test_lab_list_requires_authentication_and_supports_search(self):
        response = self.client.get(reverse("labs:lab-list"))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('labs:lab-list')}"
        )

        user = User.objects.create_user(username="viewer", password="safe-password")
        permission = Permission.objects.get(
            content_type__app_label="labs", codename="view_lab"
        )
        user.user_permissions.add(permission)
        self.client.force_login(user)
        response = self.client.get(reverse("labs:lab-list"), {"q": "Networking"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Networking Lab")
        self.assertNotContains(response, "No labs match")

    def test_related_computer_prevents_lab_deletion(self):
        Computer.objects.create(lab=self.lab, computer_number="PC-01")
        user = User.objects.create_user(username="manager", password="safe-password")
        user.user_permissions.add(
            Permission.objects.get(
                content_type__app_label="labs", codename="delete_lab"
            ),
            Permission.objects.get(
                content_type__app_label="labs", codename="view_lab"
            ),
        )
        self.client.force_login(user)
        response = self.client.post(
            reverse("labs:lab-delete", args=[self.lab.pk]), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Lab.objects.filter(pk=self.lab.pk).exists())
        self.assertContains(response, "cannot be deleted")
