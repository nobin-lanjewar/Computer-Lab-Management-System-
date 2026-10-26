from django import forms

from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["student_id", "name", "class_department", "email", "phone"]
