from django.contrib import admin

from .models import Computer, Lab, MaintenanceRecord


@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ("name", "room_number", "capacity", "is_active")
    search_fields = ("name", "room_number")
    list_filter = ("is_active",)


@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ("computer_number", "computer_name", "lab", "status")
    list_filter = ("lab", "status")
    search_fields = ("computer_number", "lab__name")


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ("computer", "reported_at", "assigned_technician", "status")
    list_filter = ("status", "reported_at")
    search_fields = ("computer__computer_number", "issue", "assigned_technician")
