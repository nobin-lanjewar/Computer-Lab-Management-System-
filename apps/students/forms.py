from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from apps.common.auth import LAB_ASSISTANT_ROLE, STUDENT_ROLE, assign_role
from .models import Student

User = get_user_model()


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


class StudentRegistrationForm(UserCreationForm):
    student_id = forms.CharField(max_length=30)
    name = forms.CharField(max_length=150)
    class_department = forms.CharField(max_length=100, label="Department / class")
    email = forms.EmailField()
    phone = forms.CharField(max_length=30, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "student_id", "name", "class_department", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields["username"].help_text = "Choose a unique username."

    def clean_student_id(self):
        student_id = self.cleaned_data["student_id"].strip()
        if Student.objects.filter(student_id__iexact=student_id).exists():
            raise forms.ValidationError("This student ID is already registered.")
        return student_id

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        if Student.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered.")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account already uses this email.")
        return email

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            student = Student.objects.create(
                user=user,
                student_id=self.cleaned_data["student_id"],
                name=self.cleaned_data["name"],
                class_department=self.cleaned_data["class_department"],
                email=self.cleaned_data["email"],
                phone=self.cleaned_data["phone"],
            )
            assign_role(user, STUDENT_ROLE)
            self.student = student
        return user


class LabAssistantCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["autocomplete"] = "email"

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.email = self.cleaned_data["email"]
            user.save(update_fields=["email"])
            assign_role(user, LAB_ASSISTANT_ROLE)
        return user
