from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from apps.common.views import ProtectedDeleteView

from .forms import StudentForm
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
