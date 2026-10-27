# Project Structure Guide

This guide describes the purpose of the important files in the Computer Lab Management System. The project uses small Django apps so each type of record has a clear home.

## Project root

- `manage.py` runs Django management commands such as `runserver`, `migrate`, `createsuperuser`, and `test`.
- `requirements.txt` lists Django and `python-dotenv`.
- `README.md` introduces the project and explains its setup, features, database, and Windows commands.
- `.gitignore` excludes virtual environments, generated Python files, the local SQLite database, local environment files, and other generated output from Git.
- `.env.example` lists environment-variable names with an empty secret value. Django loads a developer's untracked `.env`, never the example file.
- `tests/` is the root package for any future project-wide tests. App-specific tests currently live beside their apps.

## Django configuration

- `config/__init__.py` marks `config` as a Python package.
- `config/settings.py` configures installed Django and project apps, middleware, templates, authentication, static files, SQLite, and environment-based secret/debug/host settings. In development a missing secret is generated temporarily; production requires an explicit key.
- `config/urls.py` is the main URL router. It connects the dashboard, lab/computer/maintenance, student, booking, login/logout, and admin URLs.
- `config/asgi.py` exposes the ASGI application for compatible servers.
- `config/wsgi.py` exposes the WSGI application for compatible servers.

## Apps

- `apps/__init__.py` makes the app collection importable as a Python package.
- Each app's `apps.py` gives Django its app configuration and display name.
- Each app's `migrations/__init__.py` marks the migration directory as a package. Run `makemigrations` to create the initial migration files from the models.
- `apps/common/views.py` supplies a shared delete view that reports protected relationships without deleting dependent data; `apps/common/auth.py` assigns built-in Django groups, permissions, and role-specific dashboard routes.

### `apps/labs/`

- `models.py` stores `Lab` records (unique name and room, positive capacity, active state), `Computer` records (per-lab unique asset number, name, specifications, operating system, and status), and `MaintenanceRecord` records.
- `views.py` provides login-protected searchable/paginated lists, permission-protected create/edit/delete views, and maintenance workflows.
- `forms.py` defines styled model forms and requires a resolution when a maintenance record is marked resolved.
- `urls.py` maps searchable list and create/edit/delete pages for labs, computers, and maintenance.
- `admin.py` registers these models and configures searchable/filterable admin listings.
- `tests.py` covers model constraints, maintenance status synchronization, authentication, and protected deletion.

### `apps/students/`

- `models.py` stores a unique student ID, name, class/department, optional email and phone contact details, and an optional one-to-one Django user account.
- `views.py` provides login-protected searchable/paginated listings and permission-protected create/edit/delete views.
- `forms.py` defines the student form.
- `urls.py` maps searchable student list and create/edit/delete pages.
- `admin.py` registers students with searchable, filterable columns.
- `tests.py` checks student ID uniqueness and case-insensitive duplicate email validation.
- `StudentRegistrationForm` creates the user with Django's `UserCreationForm`, stores the related student profile, and assigns the Student group. The Lab Assistant account form is available only to superusers.

### `apps/schedules/`

- `models.py` stores booking date, time range, purpose, status, requester, and relationships to lab, optional computer/student, or class name. It checks time ranges, lab/computer consistency, maintenance status, required audience, and conflicts.
- `views.py` provides login-protected searchable/paginated listings and permission-protected booking request/edit/delete views.
- `forms.py` defines styled date/time controls; users with schedule-change permission can set booking status and audience.
- `urls.py` maps searchable booking list and create/edit/delete pages.
- `admin.py` registers schedules with useful columns, filters, and search.
- `tests.py` checks audience requirements, lab/computer consistency, overlap rejection, cancellation, time validation, maintenance availability, and booking permissions.

Schedule overlap checks run through model validation on every save. They prevent ordinary conflicting form submissions but do not guarantee serialization under concurrent writes, especially on SQLite. A deployed multi-user system should use transaction-safe enforcement appropriate to its production database.

Listing pages require their corresponding Django `view` permission. Student users see only bookings attributed to their account and may submit booking requests; grant assistant groups the relevant add/change/delete permissions. Users and group membership are provisioned by administrators. Deleting a student profile linked to a login account is protected to prevent orphaning an active Student role.

### `apps/dashboard/`

- `views.py` routes users to separate Admin, Lab Assistant, and Student dashboards and calculates their role-appropriate context.
- `urls.py` maps the role dashboard routes and the role-aware landing page.
- `tests.py` checks login/logout, role-based dashboards, assistant creation, and database-backed dashboard statistics.

## Templates

- `templates/base.html` contains the shared HTML structure, navigation, Bootstrap stylesheet/script links, and project static-file links.
- `templates/confirm_delete.html` confirms destructive actions before a protected server-side delete.
- `templates/includes/pagination.html` renders the shared query-preserving pagination controls.
- `templates/registration/login.html` displays Django's built-in login form.
- `templates/registration/register.html` provides student self-registration; `lab_assistant_form.html` provides the superuser-only assistant creation form.
- `templates/dashboard/index.html` displays the summary counts.
- `templates/dashboard/student.html` displays the authenticated student's profile and own booking history.
- `templates/labs/lab_list.html`, `computer_list.html`, and `maintenance_list.html` display searchable equipment records.
- `templates/labs/lab_form.html`, `computer_form.html`, and `maintenance_form.html` display management forms.
- `templates/students/student_list.html` and `student_form.html` display student records and the student create form.
- `templates/schedules/schedule_list.html` and `schedule_form.html` display and manage booking records.

## Static files

- `static/css/style.css` contains the project's small set of layout and form styles.
- `static/js/main.js` adds Bootstrap form-control styling to fields in project forms.
- `static/images/.gitkeep` keeps the otherwise-empty images directory in Git until project-owned images are added.

## Database and design decisions

SQLite is the default database and its local `db.sqlite3` file is ignored by Git. New migrations add fields and tables without recreating the database. Protected foreign keys prevent accidental deletion of labs, computers, or students with dependent records. A schedule can target one computer or reserve an entire lab by leaving its computer empty. An entire-lab booking conflicts with any overlapping active booking in that lab; a computer booking conflicts with the same computer and with an entire-lab booking. Cancelled bookings do not conflict.
