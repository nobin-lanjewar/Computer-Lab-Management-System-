from django.db import models


class Lab(models.Model):
    name = models.CharField(max_length=100, unique=True)
    room_number = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.room_number})"


class Computer(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        IN_USE = "in_use", "In Use"
        UNDER_MAINTENANCE = "under_maintenance", "Under Maintenance"

    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, related_name="computers")
    computer_number = models.CharField(max_length=30)
    specifications = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.AVAILABLE
    )

    class Meta:
        ordering = ["lab", "computer_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["lab", "computer_number"],
                name="unique_computer_number_per_lab",
            )
        ]

    def __str__(self):
        return f"{self.lab.name} - {self.computer_number}"
