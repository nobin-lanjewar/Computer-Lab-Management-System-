from django import forms

from .models import Student


class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Student
        fields = ["student_id", "name", "class_department", "email", "phone"]

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        if email and Student.objects.filter(email__iexact=email).exclude(
            pk=self.instance.pk
        ).exists():
            raise forms.ValidationError("A student with this email already exists.")
        return email
