from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.views.generic import CreateView, ListView, UpdateView

from apps.common.views import ProtectedDeleteView

from .forms import LabScheduleForm
from .models import LabSchedule


class ScheduleListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = LabSchedule
    template_name = "schedules/schedule_list.html"
    context_object_name = "schedules"
    paginate_by = 10
    permission_required = "schedules.view_labschedule"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = LabSchedule.Status.choices
        return context

    def get_queryset(self):
        queryset = LabSchedule.objects.select_related(
            "lab", "computer", "student", "requester"
        )
        if not self.request.user.has_perm("schedules.change_labschedule"):
            queryset = queryset.filter(requester=self.request.user)
        query = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "")
        date = self.request.GET.get("date", "")
        if query:
            queryset = queryset.filter(
                Q(lab__name__icontains=query)
                | Q(computer__computer_number__icontains=query)
                | Q(student__name__icontains=query)
                | Q(class_name__icontains=query)
                | Q(purpose__icontains=query)
            )
        if status in LabSchedule.Status.values:
            queryset = queryset.filter(status=status)
        if parse_date(date):
            queryset = queryset.filter(date=date)
        return queryset


class ScheduleCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = LabSchedule
    form_class = LabScheduleForm
    template_name = "schedules/schedule_form.html"
    success_url = reverse_lazy("schedules:schedule-list")
    permission_required = "schedules.add_labschedule"
    success_message = "Booking request submitted."
    extra_context = {"page_title": "Request a lab booking", "submit_label": "Submit request"}

    def get_success_url(self):
        if self.request.user.has_perm("schedules.view_labschedule"):
            return str(self.success_url)
        return str(reverse_lazy("dashboard:index"))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.requester = self.request.user
        return super().form_valid(form)


class ScheduleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = LabSchedule
    form_class = LabScheduleForm
    template_name = "schedules/schedule_form.html"
    success_url = reverse_lazy("schedules:schedule-list")
    permission_required = "schedules.change_labschedule"
    success_message = "Booking updated."
    extra_context = {"page_title": "Edit lab booking", "submit_label": "Save changes"}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ScheduleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, ProtectedDeleteView):
    model = LabSchedule
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("schedules:schedule-list")
    permission_required = "schedules.delete_labschedule"
    extra_context = {"page_title": "Delete lab booking"}
