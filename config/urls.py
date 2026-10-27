from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from apps.dashboard.views import RoleLoginView
from apps.students.views import LabAssistantCreateView, StudentRegistrationView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", RoleLoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "accounts/register/",
        StudentRegistrationView.as_view(),
        name="student-register",
    ),
    path(
        "accounts/lab-assistants/new/",
        LabAssistantCreateView.as_view(),
        name="lab-assistant-create",
    ),
    path("", include("apps.dashboard.urls")),
    path("labs/", include("apps.labs.urls")),
    path("students/", include("apps.students.urls")),
    path("schedules/", include("apps.schedules.urls")),
]
