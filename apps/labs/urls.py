from django.urls import path

from . import views

app_name = "labs"

urlpatterns = [
    path("", views.LabListView.as_view(), name="lab-list"),
    path("new/", views.LabCreateView.as_view(), name="lab-create"),
    path("computers/", views.ComputerListView.as_view(), name="computer-list"),
    path(
        "computers/new/",
        views.ComputerCreateView.as_view(),
        name="computer-create",
    ),
]
