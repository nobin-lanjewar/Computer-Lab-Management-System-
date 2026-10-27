from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class LabSchedule(models.Model):
    lab = models.ForeignKey(
        "labs.Lab", on_delete=models.CASCADE, related_name="schedules"
    )
    computer = models.ForeignKey(
        "labs.Computer",
        on_delete=models.CASCADE,
        related_name="schedules",
        blank=True,
        null=True,
    )
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="schedules",
        blank=True,
        null=True,
    )
    class_name = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    purpose = models.CharField(max_length=200)

    class Meta:
        ordering = ["date", "start_time"]
        constraints = [
            models.CheckConstraint(
                condition=Q(start_time__lt=models.F("end_time")),
                name="schedule_end_after_start",
            )
        ]

    def clean(self):
        super().clean()
        errors = {}

        if self.start_time and self.end_time and self.start_time >= self.end_time:
            errors["end_time"] = "End time must be later than start time."

        if not self.student_id and not self.class_name.strip():
            errors["class_name"] = "Select a student or enter a class name."

        if (
            self.computer_id
            and self.lab_id
            and self.computer.lab_id != self.lab_id
        ):
            errors["computer"] = "The selected computer must belong to this lab."

        if (
            not errors
            and self.lab_id
            and self.date
            and self.start_time
            and self.end_time
        ):
            overlapping = LabSchedule.objects.filter(
                lab_id=self.lab_id,
                date=self.date,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time,
            )
            if self.pk:
                overlapping = overlapping.exclude(pk=self.pk)

            if self.computer_id:
                overlapping = overlapping.filter(
                    Q(computer_id=self.computer_id) | Q(computer__isnull=True)
                )

            if overlapping.exists():
                errors["__all__"] = (
                    "This time overlaps an existing booking for the selected "
                    "computer or lab."
                )

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        target = self.computer or self.lab
        return f"{target} on {self.date} ({self.start_time}-{self.end_time})"
