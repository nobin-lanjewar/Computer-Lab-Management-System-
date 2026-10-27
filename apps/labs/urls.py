from django.urls import path

from . import views

app_name = "labs"

urlpatterns = [
    path("", views.LabListView.as_view(), name="lab-list"),
    path("new/", views.LabCreateView.as_view(), name="lab-create"),
    path("<int:pk>/edit/", views.LabUpdateView.as_view(), name="lab-update"),
    path("<int:pk>/delete/", views.LabDeleteView.as_view(), name="lab-delete"),
    path("computers/", views.ComputerListView.as_view(), name="computer-list"),
    path(
        "computers/new/",
        views.ComputerCreateView.as_view(),
        name="computer-create",
    ),
    path("computers/<int:pk>/edit/", views.ComputerUpdateView.as_view(), name="computer-update"),
    path("computers/<int:pk>/delete/", views.ComputerDeleteView.as_view(), name="computer-delete"),
    path("maintenance/", views.MaintenanceListView.as_view(), name="maintenance-list"),
    path("maintenance/new/", views.MaintenanceCreateView.as_view(), name="maintenance-create"),
    path("maintenance/<int:pk>/edit/", views.MaintenanceUpdateView.as_view(), name="maintenance-update"),
    path("maintenance/<int:pk>/delete/", views.MaintenanceDeleteView.as_view(), name="maintenance-delete"),
]
