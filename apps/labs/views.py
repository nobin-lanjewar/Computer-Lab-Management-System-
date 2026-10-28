from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from apps.common.views import ProtectedDeleteView

from .forms import ComputerForm, LabForm, MaintenanceRecordForm
from .models import Computer, Lab, MaintenanceRecord


class LabListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Lab
    template_name = "labs/lab_list.html"
    context_object_name = "labs"
    paginate_by = 10
    permission_required = "labs.view_lab"

    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            computer_count=Count("computers")
        ).order_by("name")
        query = self.request.GET.get("q", "").strip()
        active = self.request.GET.get("active", "")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(room_number__icontains=query)
                | Q(description__icontains=query)
            )
        if active in {"true", "false"}:
            queryset = queryset.filter(is_active=active == "true")
        return queryset


class LabCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Lab
    form_class = LabForm
    template_name = "labs/lab_form.html"
    success_url = reverse_lazy("labs:lab-list")
    permission_required = "labs.add_lab"
    success_message = "Lab added."
    extra_context = {"page_title": "Add lab", "submit_label": "Save lab"}


class LabUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Lab
    form_class = LabForm
    template_name = "labs/lab_form.html"
    success_url = reverse_lazy("labs:lab-list")
    permission_required = "labs.change_lab"
    success_message = "Lab updated."
    extra_context = {"page_title": "Edit lab", "submit_label": "Save changes"}


class LabDeleteView(LoginRequiredMixin, PermissionRequiredMixin, ProtectedDeleteView):
    model = Lab
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("labs:lab-list")
    permission_required = "labs.delete_lab"
    extra_context = {"page_title": "Delete lab"}


class ComputerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Computer
    template_name = "labs/computer_list.html"
    context_object_name = "computers"
    paginate_by = 10
    permission_required = "labs.view_computer"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["labs"] = Lab.objects.all()
        context["status_choices"] = Computer.Status.choices
        return context

    def get_queryset(self):
        queryset = Computer.objects.select_related("lab")
        query = self.request.GET.get("q", "").strip()
        lab_id = self.request.GET.get("lab", "")
        status = self.request.GET.get("status", "")
        if query:
            queryset = queryset.filter(
                Q(computer_number__icontains=query)
                | Q(computer_name__icontains=query)
                | Q(operating_system__icontains=query)
                | Q(specifications__icontains=query)
                | Q(lab__name__icontains=query)
            )
        if lab_id.isdigit():
            queryset = queryset.filter(lab_id=lab_id)
        if status in Computer.Status.values:
            queryset = queryset.filter(status=status)
        return queryset


class ComputerCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Computer
    form_class = ComputerForm
    template_name = "labs/computer_form.html"
    success_url = reverse_lazy("labs:computer-list")
    permission_required = "labs.add_computer"
    success_message = "Computer added."
    extra_context = {"page_title": "Add computer", "submit_label": "Save computer"}


class ComputerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Computer
    form_class = ComputerForm
    template_name = "labs/computer_form.html"
    success_url = reverse_lazy("labs:computer-list")
    permission_required = "labs.change_computer"
    success_message = "Computer updated."
    extra_context = {"page_title": "Edit computer", "submit_label": "Save changes"}


class ComputerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, ProtectedDeleteView):
    model = Computer
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("labs:computer-list")
    permission_required = "labs.delete_computer"
    extra_context = {"page_title": "Delete computer"}


class MaintenanceListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MaintenanceRecord
    template_name = "labs/maintenance_list.html"
    context_object_name = "records"
    paginate_by = 10
    permission_required = "labs.view_maintenancerecord"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = MaintenanceRecord.Status.choices
        return context

    def get_queryset(self):
        queryset = MaintenanceRecord.objects.select_related("computer", "computer__lab")
        query = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "")
        if query:
            queryset = queryset.filter(
                Q(issue__icontains=query)
                | Q(assigned_technician__icontains=query)
                | Q(computer__computer_number__icontains=query)
                | Q(computer__lab__name__icontains=query)
            )
        if status in MaintenanceRecord.Status.values:
            queryset = queryset.filter(status=status)
        return queryset


class MaintenanceCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = MaintenanceRecord
    form_class = MaintenanceRecordForm
    template_name = "labs/maintenance_form.html"
    success_url = reverse_lazy("labs:maintenance-list")
    permission_required = "labs.add_maintenancerecord"
    success_message = "Maintenance record added."
    extra_context = {"page_title": "Report maintenance", "submit_label": "Save record"}


class MaintenanceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = MaintenanceRecord
    form_class = MaintenanceRecordForm
    template_name = "labs/maintenance_form.html"
    success_url = reverse_lazy("labs:maintenance-list")
    permission_required = "labs.change_maintenancerecord"
    success_message = "Maintenance record updated."
    extra_context = {"page_title": "Update maintenance", "submit_label": "Save changes"}


class MaintenanceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, ProtectedDeleteView):
    model = MaintenanceRecord
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("labs:maintenance-list")
    permission_required = "labs.delete_maintenancerecord"
    extra_context = {"page_title": "Delete maintenance record"}
