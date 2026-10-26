from django.urls import path

from . import views

app_name = "schedules"

urlpatterns = [
    path("", views.ScheduleListView.as_view(), name="schedule-list"),
    path("new/", views.ScheduleCreateView.as_view(), name="schedule-create"),
]
