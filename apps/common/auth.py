from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group, Permission
from django.urls import reverse


STUDENT_ROLE = "Students"
LAB_ASSISTANT_ROLE = "Lab Assistants"


def dashboard_url_for(user):
    if user.is_superuser:
        return reverse("dashboard:admin")
    if user.groups.filter(name=LAB_ASSISTANT_ROLE).exists():
        return reverse("dashboard:lab-assistant")
    if user.groups.filter(name=STUDENT_ROLE).exists():
        return reverse("dashboard:student")
    raise PermissionDenied("This account has not been assigned an application role.")


def assign_role(user, role):
    group, _ = Group.objects.get_or_create(name=role)
    if role == STUDENT_ROLE:
        permissions = [
            ("labs", "view_lab"),
            ("labs", "view_computer"),
            ("schedules", "add_labschedule"),
            ("schedules", "view_labschedule"),
        ]
    elif role == LAB_ASSISTANT_ROLE:
        permissions = [
            (app_label, f"{action}_{model}")
            for app_label, model in (
                ("labs", "lab"),
                ("labs", "computer"),
                ("labs", "maintenancerecord"),
                ("students", "student"),
                ("schedules", "labschedule"),
            )
            for action in ("view", "add", "change", "delete")
        ]
    else:
        raise ValueError(f"Unsupported role: {role}")

    group.permissions.add(
        *[
            Permission.objects.get(
                content_type__app_label=app_label,
                codename=codename,
            )
            for app_label, codename in permissions
        ]
    )
    user.groups.add(group)
