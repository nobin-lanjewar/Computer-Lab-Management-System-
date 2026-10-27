from django.urls import path

from .views import (
    AdminDashboardView,
    DashboardView,
    LabAssistantDashboardView,
    StudentDashboardView,
)

app_name = "dashboard"

urlpatterns = [
    path("", DashboardView.as_view(), name="index"),
    path("administrator/", AdminDashboardView.as_view(), name="admin"),
    path("lab-assistant/", LabAssistantDashboardView.as_view(), name="lab-assistant"),
    path("student/", StudentDashboardView.as_view(), name="student"),
]
