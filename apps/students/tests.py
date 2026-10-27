from django.core.exceptions import ValidationError
from django.test import TestCase

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
