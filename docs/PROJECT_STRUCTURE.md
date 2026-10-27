# Project Structure Guide

This guide describes the purpose of the important files in the Computer Lab Management System. The project uses small Django apps so each type of record has a clear home.

## Project root

- `manage.py` runs Django management commands such as `runserver`, `migrate`, `createsuperuser`, and `test`.
- `requirements.txt` lists the Python packages needed to install the project. Django is the only required package.
- `README.md` introduces the project and explains its setup, features, database, and Windows commands.
- `.gitignore` excludes virtual environments, generated Python files, the local SQLite database, local environment files, and other generated output from Git.
- `.env.example` lists environment-variable names with safe placeholders. It is a reference, not a real secret file, and Django does not load it automatically.
- `tests/` is the root package for any future project-wide tests. App-specific tests currently live beside their apps.

## Django configuration

- `config/__init__.py` marks `config` as a Python package.
- `config/settings.py` configures installed Django and project apps, middleware, templates, authentication, static files, SQLite, and environment-based secret/debug/host settings.
- `config/urls.py` is the main URL router. It connects the dashboard, lab/computer, student, schedule, login/logout, and admin URLs.
- `config/asgi.py` exposes the ASGI application for compatible servers.
- `config/wsgi.py` exposes the WSGI application for compatible servers.

## Apps

- `apps/__init__.py` makes the app collection importable as a Python package.
- Each app's `apps.py` gives Django its app configuration and display name.
- Each app's `migrations/__init__.py` marks the migration directory as a package. Run `makemigrations` to create the initial migration files from the models.

### `apps/labs/`

- `models.py` stores `Lab` records (unique name and room number, description) and `Computer` records (number, lab relationship, specifications, and Available/In Use/Under Maintenance status). A computer number is unique within its lab.
- `views.py` displays and creates labs and computers. Editing and deleting through custom pages are future work; Django admin currently provides record management.
- `forms.py` defines the lab and computer forms and their model-backed validation.
- `urls.py` maps lab and computer list/create pages.
- `admin.py` registers labs and computers and configures useful admin columns, filters, and search.
- `tests.py` checks computer default status and its per-lab number constraint.

### `apps/students/`

- `models.py` stores a unique student ID, name, class/department, and optional email and phone contact details.
- `views.py` displays and creates student records. Custom edit/delete pages are future work.
- `forms.py` defines the student form.
- `urls.py` maps student list/create pages.
- `admin.py` registers students with searchable, filterable columns.
- `tests.py` checks student ID uniqueness.

### `apps/schedules/`

- `models.py` stores schedule date, start/end time, purpose, and relationships to a lab, optional computer, optional student, and optional class name. It checks that a computer belongs to the selected lab, that a student or class is specified, that the end follows the start, and that relevant bookings do not overlap.
- `views.py` displays and creates lab schedules. Custom edit/delete pages are future work.
- `forms.py` defines the schedule form and browser date/time controls; Django model validation is applied when the form is validated.
- `urls.py` maps schedule list/create pages.
- `admin.py` registers schedules with useful columns, filters, and search.
- `tests.py` checks audience requirements, lab/computer consistency, overlap rejection, and adjacent non-overlapping bookings.

Schedule overlap checks are application validation, not database exclusion constraints. They prevent ordinary conflicting form submissions but do not guarantee safety under concurrent writes. A deployed multi-user system should add transaction-safe enforcement.

### `apps/dashboard/`

- `views.py` calculates lab, computer, available-computer, student, and schedule counts for the dashboard.
- `urls.py` maps the dashboard to the site root.
- `tests.py` checks that the dashboard responds and includes its availability summary.

## Templates

- `templates/base.html` contains the shared HTML structure, navigation, Bootstrap stylesheet/script links, and project static-file links.
- `templates/registration/login.html` displays Django's built-in login form.
- `templates/dashboard/index.html` displays the summary counts.
- `templates/labs/lab_list.html` and `computer_list.html` display lab and computer records.
- `templates/labs/lab_form.html` and `computer_form.html` display the lab and computer create forms.
- `templates/students/student_list.html` and `student_form.html` display student records and the student create form.
- `templates/schedules/schedule_list.html` and `schedule_form.html` display schedule records and the schedule create form.

## Static files

- `static/css/style.css` contains the project's small set of layout and form styles.
- `static/js/main.js` adds Bootstrap form-control styling to fields in project forms.
- `static/images/.gitkeep` keeps the otherwise-empty images directory in Git until project-owned images are added.

## Database and design decisions

SQLite is the default database and its local `db.sqlite3` file is generated by migrations and ignored by Git. Foreign keys avoid duplicating lab/computer/student details in schedules. Computer numbers are unique within a lab; lab names, room numbers, and student IDs are unique. A schedule can target one computer or reserve an entire lab by leaving its computer empty. If a student is not selected, a class name is required. An entire-lab booking conflicts with any overlapping booking in that lab; a computer booking conflicts with the same computer and with an entire-lab booking.
