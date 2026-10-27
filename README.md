# Computer Lab Management System

A Django web application for managing laboratory spaces, computers, students, lab bookings, and computer maintenance. The existing Django apps and database are extended in place; migrations preserve existing records.

## Features

- Database-backed dashboard statistics and upcoming booking list.
- Lab and computer create, view, edit, and delete workflows.
- Student directory with unique student IDs and case-insensitive duplicate email validation.
- Booking requests with requester attribution, requested/approved/cancelled status, date and status filters, and server-side conflict validation.
- Maintenance history with pending, in-progress, and resolved states; active maintenance automatically marks a computer unavailable.
- Search, filters, and pagination on lab, computer, student, booking, and maintenance listings.
- Django built-in login/logout, password validation, sessions, and password hashing.
- Student self-registration, with unique student profile IDs and automatic Student role assignment.
- Admin-created Lab Assistant accounts and automatic group-based permissions.
- Separate Admin, Lab Assistant, and Student dashboards with role-based server-side access.
- Login-required pages and Django model permissions for record creation, editing, and deletion.
- Protected relationships prevent deleting labs, computers, or students that are still referenced.
- Django admin for staff users and responsive Bootstrap 5 pages.

Students can register through the public registration page. Admin accounts are created only with Django's `createsuperuser` command; logged-in superusers can create Lab Assistant accounts from the application.

## Technology

- Python 3.10+
- Django 5.2 or newer, below 7
- SQLite for local development
- HTML, CSS, JavaScript, and Bootstrap 5
- `python-dotenv` for optional local `.env` configuration

## Project structure

```text
config/                 Django settings and root URLs
apps/common/            Shared protected-delete behavior
apps/dashboard/         Database-backed dashboard
apps/labs/              Labs, computers, maintenance, and related forms
apps/students/          Student records
apps/schedules/         Lab bookings and overlap validation
templates/              Shared layout and app pages
static/                 Project CSS and JavaScript
docs/                   Project structure notes
manage.py               Django command-line entry point
requirements.txt        Python dependencies
```

## Windows setup

Run these commands from the repository root, next to `manage.py`.

### 1. Create and activate a virtual environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, allow it for the current terminal only:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
```

Command Prompt users can run:

```bat
.venv\Scripts\activate.bat
```

### 2. Install dependencies

```powershell
py -m pip install -r requirements.txt
```

### 3. Configure development environment

Copy the example file and generate a local secret key. Keep `.env` private and do not commit it.

```powershell
Copy-Item .env.example .env
$env:DJANGO_SECRET_KEY = py -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
$env:DJANGO_DEBUG = "True"
$env:DJANGO_ALLOWED_HOSTS = "127.0.0.1,localhost"
```

These `$env:` values apply to the current PowerShell session. For repeat use, put a generated key and the desired values in `.env`; `.env.example` intentionally contains no secret. If `DJANGO_SECRET_KEY` is omitted in development, Django generates a temporary development key. Production mode (`DJANGO_DEBUG=False`) requires an explicit secret key.

### 4. Inspect and apply migrations

Before applying migrations to an existing local database, inspect the migration state:

```powershell
py manage.py showmigrations
```

The supplied migration changes are additive and include defaults for the new fields. Apply them without deleting or recreating `db.sqlite3`:

```powershell
py manage.py migrate
```

### 5. Create an administrator and run

```powershell
py manage.py createsuperuser
py manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and sign in. Students can register at [http://127.0.0.1:8000/accounts/register/](http://127.0.0.1:8000/accounts/register/). The Django admin is at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

## Roles and permissions

Authentication uses Django's built-in users, groups, model permissions, sessions, password hashing, and password validators. Roles are assigned with built-in groups:

- **Admin:** create with `createsuperuser`. Only superusers can use the in-app Lab Assistant account creation page.
- **Lab Assistant:** created by a superuser. The account receives the Lab Assistants group and record-management permissions; it is not granted Django `is_staff` or superuser access.
- **Student:** self-registration creates a linked Student profile and adds the Students group. Students can request lab bookings and see only their own booking records.

After login, Django redirects each role to its separate dashboard. Role dashboard routes and all record views enforce access server-side; hiding a navigation link is not used as a permission check. Users created manually in Django admin should be assigned the appropriate group.

## Testing and checks

Activate the virtual environment and configure `DJANGO_SECRET_KEY`, then run:

```powershell
py manage.py check
py manage.py test
py manage.py makemigrations --check --dry-run
```

Tests cover permissions, CRUD-related protections, database-driven dashboard statistics, maintenance status transitions, email validation, booking time validation, and overlapping bookings.

## Data and booking behavior

- A computer's asset number (`computer_number`) is unique within its lab. Lab room number and name, and student ID, are unique.
- Lab capacity must be positive. Mark unused labs inactive rather than deleting them.
- Schedules can book a specific computer or an entire lab. End times must follow start times; overlapping active requests/approved bookings are rejected. Cancelled bookings do not block later bookings.
- A computer under maintenance cannot be booked. Creating or activating maintenance marks it under maintenance; resolving the last active maintenance record restores it to Available.
- Labs, computers, and students with related records cannot be deleted until those relationships are removed. A clear message is shown rather than cascading data loss.
- Application validation checks booking conflicts on every server-side save. If deploying with concurrent writers, use a database and transaction strategy suitable for serialization; SQLite is intended for local development.

## Security and deployment notes

- Never commit `.env`, a production secret key, or a real database.
- `DEBUG` defaults to development mode. Set `DJANGO_DEBUG=False`, configure a strong `DJANGO_SECRET_KEY`, and set `DJANGO_ALLOWED_HOSTS` before production use.
- Configure HTTPS, secure cookies, static-file serving, backups, and a production-grade database before deployment.
- Bootstrap is loaded from its public CDN; the app's custom CSS and JavaScript are served locally.
