from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Computer, Lab


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
