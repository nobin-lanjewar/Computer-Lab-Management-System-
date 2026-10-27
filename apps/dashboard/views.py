from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView

from apps.labs.models import Computer, Lab
from apps.schedules.models import LabSchedule
from apps.students.models import Student


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lab_count"] = Lab.objects.count()
        context["computer_count"] = Computer.objects.count()
        context["available_computer_count"] = Computer.objects.filter(
            status=Computer.Status.AVAILABLE
        ).count()
        context["maintenance_computer_count"] = Computer.objects.filter(
            status=Computer.Status.UNDER_MAINTENANCE
        ).count()
        context["student_count"] = Student.objects.count()
        schedules = LabSchedule.objects.all()
        if not self.request.user.has_perm("schedules.change_labschedule"):
            schedules = schedules.filter(requester=self.request.user)
        context["upcoming_schedules"] = (
            schedules.filter(
                date__gte=timezone.localdate(),
                status__in=[
                    LabSchedule.Status.REQUESTED,
                    LabSchedule.Status.APPROVED,
                ],
            )
            .select_related("lab", "computer", "student")
            .order_by("date", "start_time")[:5]
        )
        context["recent_schedules"] = (
            schedules.select_related("lab", "requester")
            .order_by("-date", "-start_time")[:5]
        )
        return context
