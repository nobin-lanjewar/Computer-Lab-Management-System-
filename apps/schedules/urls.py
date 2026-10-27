from django.urls import path

from . import views

app_name = "schedules"

urlpatterns = [
    path("", views.ScheduleListView.as_view(), name="schedule-list"),
    path("new/", views.ScheduleCreateView.as_view(), name="schedule-create"),
    path("<int:pk>/edit/", views.ScheduleUpdateView.as_view(), name="schedule-update"),
    path("<int:pk>/delete/", views.ScheduleDeleteView.as_view(), name="schedule-delete"),
]
