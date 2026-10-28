from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from apps.common.auth import (
    LAB_ASSISTANT_ROLE,
    STUDENT_ROLE,
    dashboard_url_for,
)
from apps.labs.models import Computer, Lab
from apps.schedules.models import LabSchedule
from apps.students.models import Student


class RoleLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def get_default_redirect_url(self):
        return dashboard_url_for(self.request.user)


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(dashboard_url_for(request.user))


class OperationsDashboardView(TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard_role"] = self.dashboard_role
        context["can_manage_bookings"] = self.request.user.has_perm(
            "schedules.change_labschedule"
        )
        context["is_admin_dashboard"] = self.dashboard_role == "Administrator"
        context["is_assistant_dashboard"] = self.dashboard_role == "Lab assistant"
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
        if not context["can_manage_bookings"]:
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


class AdminDashboardView(
    LoginRequiredMixin, UserPassesTestMixin, OperationsDashboardView
):
    dashboard_role = "Administrator"

    def test_func(self):
        return self.request.user.is_superuser


class LabAssistantDashboardView(
    LoginRequiredMixin, UserPassesTestMixin, OperationsDashboardView
):
    dashboard_role = "Lab assistant"

    def test_func(self):
        return (
            not self.request.user.is_superuser
            and self.request.user.groups.filter(name=LAB_ASSISTANT_ROLE).exists()
        )


class StudentDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboard/student.html"

    def test_func(self):
        return (
            not self.request.user.is_superuser
            and self.request.user.groups.filter(name=STUDENT_ROLE).exists()
            and Student.objects.filter(user=self.request.user).exists()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.student_profile
        context["student"] = profile
        context["bookings"] = (
            LabSchedule.objects.filter(requester=self.request.user)
            .select_related("lab", "computer")
            .order_by("-date", "-start_time")[:10]
        )
        return context
