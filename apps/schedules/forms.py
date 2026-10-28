from django import forms

from apps.students.models import Student

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
            "status",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        can_manage = user and user.has_perm("schedules.change_labschedule")
        self.student_profile = (
            Student.objects.filter(user=user).first() if user else None
        )
        if not can_manage:
            self.fields.pop("status", None)
            self.fields.pop("student", None)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super().clean()
        if self.student_profile:
            self.instance.student = self.student_profile
        return cleaned_data
