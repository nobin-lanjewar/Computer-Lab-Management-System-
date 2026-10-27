from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q


class Lab(models.Model):
    name = models.CharField(max_length=100, unique=True)
    room_number = models.CharField(max_length=30, unique=True)
    capacity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.room_number})"


class Computer(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        IN_USE = "in_use", "In Use"
        UNDER_MAINTENANCE = "under_maintenance", "Under Maintenance"

    lab = models.ForeignKey(Lab, on_delete=models.PROTECT, related_name="computers")
    computer_number = models.CharField(max_length=30)
    computer_name = models.CharField(max_length=100, blank=True)
    specifications = models.TextField(blank=True)
    operating_system = models.CharField(max_length=100, blank=True)
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

    def save(self, *args, **kwargs):
        if self.pk and self.maintenance_records.exclude(
            status=MaintenanceRecord.Status.RESOLVED
        ).exists():
            self.status = self.Status.UNDER_MAINTENANCE
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.lab.name} - {self.computer_number}"


class MaintenanceRecord(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        RESOLVED = "resolved", "Resolved"

    computer = models.ForeignKey(
        Computer, on_delete=models.PROTECT, related_name="maintenance_records"
    )
    issue = models.TextField()
    reported_at = models.DateField(auto_now_add=True)
    assigned_technician = models.CharField(max_length=150, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    resolution = models.TextField(blank=True)

    class Meta:
        ordering = ["-reported_at", "-pk"]
        indexes = [models.Index(fields=["status", "reported_at"])]

    def clean(self):
        super().clean()
        if (
            self.status == self.Status.RESOLVED
            and not self.resolution.strip()
        ):
            raise ValidationError(
                {"resolution": "Add a resolution before closing maintenance."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        old_computer_id = None
        if self.pk:
            old_computer_id = (
                type(self).objects.filter(pk=self.pk)
                .values_list("computer_id", flat=True)
                .first()
            )
        super().save(*args, **kwargs)
        self._sync_computer_status(self.computer_id)
        if old_computer_id and old_computer_id != self.computer_id:
            self._sync_computer_status(old_computer_id)

    def delete(self, *args, **kwargs):
        computer_id = self.computer_id
        result = super().delete(*args, **kwargs)
        self._sync_computer_status(computer_id)
        return result

    @staticmethod
    def _sync_computer_status(computer_id):
        active_maintenance = MaintenanceRecord.objects.filter(
            computer_id=computer_id
        ).exclude(status=MaintenanceRecord.Status.RESOLVED).exists()
        if active_maintenance:
            Computer.objects.filter(pk=computer_id).update(
                status=Computer.Status.UNDER_MAINTENANCE
            )
        else:
            Computer.objects.filter(
                pk=computer_id, status=Computer.Status.UNDER_MAINTENANCE
            ).update(status=Computer.Status.AVAILABLE)

    def __str__(self):
        return f"{self.computer} maintenance ({self.get_status_display()})"
