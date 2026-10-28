from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, ListView, UpdateView

from apps.common.auth import dashboard_url_for
from apps.common.views import ProtectedDeleteView

from .forms import (
    LabAssistantCreationForm,
    StudentForm,
    StudentRegistrationForm,
)
from .models import Student


class StudentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = "students"
    paginate_by = 10
    permission_required = "students.view_student"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(
                Q(student_id__icontains=query)
                | Q(name__icontains=query)
                | Q(class_department__icontains=query)
                | Q(email__icontains=query)
            )
        return queryset


class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = "students/student_form.html"
    success_url = reverse_lazy("students:student-list")
    permission_required = "students.add_student"
    success_message = "Student added."
    extra_context = {"page_title": "Add student", "submit_label": "Save student"}


class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "students/student_form.html"
    success_url = reverse_lazy("students:student-list")
    permission_required = "students.change_student"
    success_message = "Student updated."
    extra_context = {"page_title": "Edit student", "submit_label": "Save changes"}


class StudentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, ProtectedDeleteView):
    model = Student
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("students:student-list")
    permission_required = "students.delete_student"
    extra_context = {"page_title": "Delete student"}


class StudentRegistrationView(FormView):
    template_name = "registration/register.html"
    form_class = StudentRegistrationForm
    success_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(dashboard_url_for(request.user))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your student account has been created.")
        return super().form_valid(form)


class LabAssistantCreateView(
    LoginRequiredMixin, UserPassesTestMixin, FormView
):
    template_name = "registration/lab_assistant_form.html"
    form_class = LabAssistantCreationForm
    success_url = reverse_lazy("dashboard:admin")

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Lab assistant account created.")
        return super().form_valid(form)
