# Computer Lab Management System

## 1. Introduction

The Computer Lab Management System is a beginner-friendly academic web application for organizing computer laboratories, computers, student records, and lab schedules. It is built with Python and Django and uses SQLite by default.

The current project is a working foundation: it includes the Django project, initial data models, Django admin, dashboard summaries, and list/create pages for the main records. It is not yet a complete production-ready management system.

## 2. Problem Statement

Keeping laboratory, computer, student, and timetable records in notebooks or separate files makes information difficult to update and check. It can also lead to duplicate records and conflicting computer bookings. A small web application can keep these records together and make them easier to review.

## 3. Objectives

- Organize labs and their computers in one application.
- Maintain student and class contact records.
- Record computer availability and planned lab use.
- Provide a simple dashboard and browser-based record pages.
- Demonstrate Django models, forms, URLs, templates, the admin site, and tests.

## 4. Features

Implemented in this initial version:

- Dashboard counts for labs, computers, students, and schedules, plus available-computer count.
- Lab, computer, student, and schedule models with basic validation and uniqueness rules.
- List and create pages for each record type.
- Django admin registration for managing all four record types.
- Schedule validation for time ranges, lab/computer consistency, audience selection, and overlapping bookings.
- Basic automated model tests.

Editing/deleting records, role-based permissions, reports, and production deployment are not implemented yet. Records can be managed through Django admin in the meantime.

## 5. Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5 (loaded from its public CDN)
- **Database:** SQLite by default
- **Version control:** Git

## 6. Complete Folder Structure

```text
Computer-Lab-Management-System-/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── apps/
│   ├── __init__.py
│   ├── labs/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   └── migrations/
│   │       └── __init__.py
│   ├── students/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   └── migrations/
│   │       └── __init__.py
│   ├── schedules/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   └── migrations/
│   │       └── __init__.py
│   └── dashboard/
│       ├── __init__.py
│       ├── apps.py
│       ├── views.py
│       ├── urls.py
│       └── tests.py
├── templates/
│   ├── base.html
│   ├── registration/
│   │   └── login.html
│   ├── dashboard/
│   │   └── index.html
│   ├── labs/
│   │   ├── computer_list.html
│   │   ├── computer_form.html
│   │   ├── lab_list.html
│   │   └── lab_form.html
│   ├── students/
│   │   ├── student_list.html
│   │   └── student_form.html
│   └── schedules/
│       ├── schedule_list.html
│       └── schedule_form.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       └── .gitkeep
├── docs/
│   └── PROJECT_STRUCTURE.md
└── tests/
    └── __init__.py
```

## 7. Explanation of Important Files

The detailed file-by-file guide is in [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md). In brief:

- `manage.py` runs Django management commands.
- `config/settings.py` configures apps, templates, static files, database, and environment-based settings.
- `config/urls.py` connects the dashboard, app pages, login, and Django admin.
- `apps/*/models.py` defines the database records; `forms.py` validates browser form input; `views.py` serves the current list/create pages; `urls.py` maps those pages; `admin.py` configures admin; and `tests.py` contains app tests.
- `templates/` contains shared layout, dashboard, login, list, and create-form pages.
- `static/` contains project CSS, JavaScript, and the images directory.
- `requirements.txt` lists Python dependencies.
- `.gitignore` excludes generated and secret files. `.env.example` documents environment variable names only.

## 8. Database Overview

The default database is SQLite, stored locally as `db.sqlite3` after the first migration. The database can be changed in `config/settings.py` if the project later needs a different database.

- **Lab:** unique lab name and room number, plus an optional description.
- **Computer:** computer number, lab foreign key, specifications, and status (`Available`, `In Use`, or `Under Maintenance`). Computer numbers are unique within a lab.
- **Student:** unique student ID, name, class/department, and optional email/phone contact details.
- **LabSchedule:** lab foreign key, optional computer and student foreign keys, optional class name, date, start/end times, and purpose. A schedule must name a student or a class. A computer must belong to the selected lab.

The models validate that a schedule ends after it starts. A lab-wide booking (no computer selected) conflicts with every booking in that lab for an overlapping time; a computer booking conflicts with another booking for the same computer and with lab-wide bookings. These checks run through Django model/form validation. They are not database-level exclusion constraints, so deployments with concurrent booking writes should add transaction-safe conflict enforcement.

## 9. Installation and Setup on Windows

Run all commands below from the repository root (the directory containing `manage.py`). If you have not cloned the project, use the actual repository URL supplied by its owner; no repository URL is assumed here.

```powershell
git clone YOUR_REPOSITORY_URL
cd Computer-Lab-Management-System-
```

## 10. Create and Activate a Virtual Environment

```powershell
py -m venv .venv
```

PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, allow scripts for this terminal session only, then activate:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.venv\Scripts\Activate.ps1
```

Command Prompt alternative:

```bat
.venv\Scripts\activate.bat
```

## 11. Install Dependencies

With the virtual environment activated, from the repository root:

```powershell
py -m pip install -r requirements.txt
```

## 12. Configure the Development Secret Key

The application reads `DJANGO_SECRET_KEY` from the environment and does not store a real key in Git. Generate a key and set it for the current PowerShell session:

```powershell
$env:DJANGO_SECRET_KEY = py -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

For optional settings, `.env.example` lists variable names and safe placeholders. Django does not load `.env` files automatically; set the variables in your shell or use an environment-variable manager. `DJANGO_DEBUG` defaults to `True` for local development. Do not use debug mode or the development server for public production hosting.

## 13. Create and Apply Database Migrations

From the repository root, create model migrations and apply them:

```powershell
py manage.py makemigrations
py manage.py migrate
```

## 14. Create a Django Superuser

```powershell
py manage.py createsuperuser
```

Follow the prompts to create the local administrator account.

## 15. Run the Development Server

```powershell
py manage.py runserver
```

## 16. Open the Application

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) for the dashboard or [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) for Django admin. The login page is at [http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/).

## 17. Run Tests

From the repository root, run the project tests:

```powershell
py manage.py test
```

## 18. Troubleshooting

- **`DJANGO_SECRET_KEY` is missing:** Set it in the same terminal session before running Django commands, as shown above.
- **`No module named django`:** Activate `.venv` and run `py -m pip install -r requirements.txt`.
- **PowerShell will not activate `.venv`:** Use the process-scoped execution policy command in the virtual-environment section, or use Command Prompt activation.
- **Database or table errors:** From the repository root, run `py manage.py migrate`.
- **Port 8000 is occupied:** Run `py manage.py runserver 8001` and open `http://127.0.0.1:8001/`.
- **Bootstrap styling does not load:** Bootstrap is served from a CDN and requires an internet connection; the project's own CSS remains local.

## 19. Future Scope

- Add edit/delete workflows and confirmation pages.
- Add user authentication and role-based permissions to management pages.
- Enforce schedule conflict checks safely during concurrent requests.
- Add search, filters, reports, and maintenance history.
- Add deployment configuration and production security settings.

## 20. Conclusion

This project provides a small, understandable Django foundation for a Computer Lab Management System. It establishes the core records and a working path for extending the application while keeping unimplemented features clearly identified.

## 21. Author

**Nobindas Lanjewar**
