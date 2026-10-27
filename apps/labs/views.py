from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import ComputerForm, LabForm
from .models import Computer, Lab


class LabListView(ListView):
    model = Lab
    template_name = "labs/lab_list.html"
    context_object_name = "labs"


class LabCreateView(CreateView):
    model = Lab
    form_class = LabForm
    template_name = "labs/lab_form.html"
    success_url = reverse_lazy("labs:lab-list")


class ComputerListView(ListView):
    model = Computer
    template_name = "labs/computer_list.html"
    context_object_name = "computers"
    queryset = Computer.objects.select_related("lab")


class ComputerCreateView(CreateView):
    model = Computer
    form_class = ComputerForm
    template_name = "labs/computer_form.html"
    success_url = reverse_lazy("labs:computer-list")
