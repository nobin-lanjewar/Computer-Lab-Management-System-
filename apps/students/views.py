from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import StudentForm
from .models import Student


class StudentListView(ListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = "students"


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = "students/student_form.html"
    success_url = reverse_lazy("students:student-list")
