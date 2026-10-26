from django.views.generic import TemplateView

from apps.labs.models import Computer, Lab
from apps.schedules.models import LabSchedule
from apps.students.models import Student


class DashboardView(TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lab_count"] = Lab.objects.count()
        context["computer_count"] = Computer.objects.count()
        context["available_computer_count"] = Computer.objects.filter(
            status=Computer.Status.AVAILABLE
        ).count()
        context["student_count"] = Student.objects.count()
        context["schedule_count"] = LabSchedule.objects.count()
        return context
