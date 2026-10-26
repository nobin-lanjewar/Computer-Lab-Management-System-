from django.db import models


class Student(models.Model):
    student_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=150)
    class_department = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ["name", "student_id"]

    def __str__(self):
        return f"{self.student_id} - {self.name}"
