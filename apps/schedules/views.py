from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import LabScheduleForm
from .models import LabSchedule


class ScheduleListView(ListView):
    model = LabSchedule
    template_name = "schedules/schedule_list.html"
    context_object_name = "schedules"
    queryset = LabSchedule.objects.select_related("lab", "computer", "student")


class ScheduleCreateView(CreateView):
    model = LabSchedule
    form_class = LabScheduleForm
    template_name = "schedules/schedule_form.html"
    success_url = reverse_lazy("schedules:schedule-list")
