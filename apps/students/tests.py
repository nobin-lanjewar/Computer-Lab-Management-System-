from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse

from apps.common.auth import STUDENT_ROLE

from .forms import StudentForm, StudentRegistrationForm
from .models import Student


class StudentModelTests(TestCase):
    def test_student_id_must_be_unique(self):
        Student.objects.create(
            student_id="ST-001", name="Asha Patil", class_department="Diploma"
        )
        duplicate = Student(
            student_id="ST-001", name="Ravi More", class_department="Diploma"
        )

        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_student_profile_cannot_be_deleted_while_user_account_is_linked(self):
        user = User.objects.create_user(username="student", password="safe-password")
        student = Student.objects.create(
            user=user,
            student_id="ST-001",
            name="Asha Patil",
            class_department="Diploma",
        )

        with self.assertRaises(ProtectedError):
            student.delete()

    def test_student_form_rejects_duplicate_email_case_insensitively(self):
        Student.objects.create(
            student_id="ST-001", name="Asha Patil",
            class_department="Diploma", email="asha@example.test",
        )
        form = StudentForm(
            data={
                "student_id": "ST-002",
                "name": "Ravi More",
                "class_department": "Diploma",
                "email": "ASHA@example.test",
                "phone": "",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_registration_creates_hashed_student_account_and_cannot_assign_admin(self):
        response = self.client.post(
            reverse("student-register"),
            {
                "username": "student01",
                "email": "student@example.test",
                "student_id": "ST-100",
                "name": "Student Example",
                "class_department": "Computing",
                "phone": "12345",
                "password1": "Strong-test-password-2026!",
                "password2": "Strong-test-password-2026!",
                "is_superuser": "on",
                "is_staff": "on",
            },
        )

        self.assertRedirects(response, reverse("login"))
        user = User.objects.get(username="student01")
        self.assertTrue(user.check_password("Strong-test-password-2026!"))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.groups.filter(name=STUDENT_ROLE).exists())
        self.assertEqual(user.student_profile.student_id, "ST-100")

    def test_registration_rejects_duplicate_student_identifier_and_email(self):
        Student.objects.create(
            student_id="ST-100",
            name="Existing Student",
            class_department="Computing",
            email="existing@example.test",
        )
        form = StudentRegistrationForm(
            data={
                "username": "newstudent",
                "email": "EXISTING@example.test",
                "student_id": "st-100",
                "name": "New Student",
                "class_department": "Computing",
                "phone": "",
                "password1": "Strong-test-password-2026!",
                "password2": "Strong-test-password-2026!",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("student_id", form.errors)
        self.assertIn("email", form.errors)

    def test_registration_page_renders_for_anonymous_users(self):
        response = self.client.get(reverse("student-register"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create your student account")
