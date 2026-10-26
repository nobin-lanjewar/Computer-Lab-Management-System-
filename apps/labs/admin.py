from django.contrib import admin

from .models import Computer, Lab


@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ("name", "room_number")
    search_fields = ("name", "room_number")


@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ("computer_number", "lab", "status")
    list_filter = ("lab", "status")
    search_fields = ("computer_number", "lab__name")
