from django.urls import path

from . import views

app_name = "students"

urlpatterns = [
    path("", views.StudentListView.as_view(), name="student-list"),
    path("new/", views.StudentCreateView.as_view(), name="student-create"),
    path("<int:pk>/edit/", views.StudentUpdateView.as_view(), name="student-update"),
    path("<int:pk>/delete/", views.StudentDeleteView.as_view(), name="student-delete"),
]
