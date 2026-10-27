from django.db import models
from django.db.models.deletion import ProtectedError
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="student_profile",
        blank=True,
        null=True,
    )
    student_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=150)
    class_department = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ["name", "student_id"]

    def __str__(self):
        return f"{self.student_id} - {self.name}"


@receiver(pre_delete, sender=Student)
def prevent_deleting_linked_student_profile(sender, instance, **kwargs):
    if instance.user_id:
        raise ProtectedError(
            "A student profile linked to a login account cannot be deleted.",
            [instance.user],
        )
