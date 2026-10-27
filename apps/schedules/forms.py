from django import forms

from .models import LabSchedule


class LabScheduleForm(forms.ModelForm):
    class Meta:
        model = LabSchedule
        fields = [
            "lab",
            "computer",
            "student",
            "class_name",
            "date",
            "start_time",
            "end_time",
            "purpose",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }
