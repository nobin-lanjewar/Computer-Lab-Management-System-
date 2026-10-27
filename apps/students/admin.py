from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "name", "class_department", "email", "phone")
    search_fields = ("student_id", "name", "class_department")
    list_filter = ("class_department",)
