from django.contrib import admin

from .models import LabSchedule


@admin.register(LabSchedule)
class LabScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "start_time",
        "end_time",
        "lab",
        "computer",
        "student",
        "class_name",
        "status",
    )
    list_filter = ("date", "lab", "status")
    search_fields = ("purpose", "class_name", "student__name", "computer__computer_number")
