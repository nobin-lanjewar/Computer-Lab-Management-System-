from django import forms

from .models import Computer, Lab, MaintenanceRecord


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = "form-check-input" if isinstance(field.widget, forms.CheckboxInput) else "form-control"
            field.widget.attrs["class"] = f"{field.widget.attrs.get('class', '')} {css_class}".strip()


class LabForm(StyledModelForm):
    class Meta:
        model = Lab
        fields = ["name", "room_number", "capacity", "description", "is_active"]
        labels = {"room_number": "Location / room"}


class ComputerForm(StyledModelForm):
    class Meta:
        model = Computer
        fields = [
            "lab",
            "computer_number",
            "computer_name",
            "specifications",
            "operating_system",
            "status",
        ]
        labels = {"computer_number": "Asset number"}


class MaintenanceRecordForm(StyledModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = [
            "computer",
            "issue",
            "assigned_technician",
            "status",
            "resolution",
        ]
