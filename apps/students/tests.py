from django.core.exceptions import ValidationError
from django.test import TestCase

from .forms import StudentForm
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
