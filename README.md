








chool SMS — Setup README (step-by-step)

Yeh README tumhare current local setup ka concise record hai — taake tum kabhi bhi wapas aao to quickly samajh sako kya kiya, kahan files hain, aur kaise run karna hai. Main simple commands, file locations, aur important snippets de raha/rahi hoon.

1. Environment / Requirements

OS: Windows with WSL (Ubuntu-24.04)

Python: 3.11 (venv ke andar)

VS Code (Remote - WSL recommended)

Package manager used: uv (project tracking) + pip (direct installs inside venv)

2. Project root

Project folder (example path used here):

/home/seherkhan/school_sms
# OR (in your case) /mnt/c/Users/user/Desktop/school


Open this folder in VS Code Remote-WSL.

3. Virtual environment

Create + activate venv:

cd ~/school_sms        # go to project folder
python3 -m venv .venv
source .venv/bin/activate
# prompt should show: (.venv) seherkhan@...:~/school_sms$


Check python in venv:

which python   # -> /home/seherkhan/school_sms/.venv/bin/python
python --version

4. Initialize uv (optional but used)
uv init
# creates pyproject.toml and uv.lock for package tracking


If uv gives trouble installing into venv, use pip inside activated venv.

5. Install dependencies

Preferred (inside active .venv):

# using pip (reliable)
pip install django djangorestframework psycopg2-binary django-htmx


Or with uv ensuring venv Python:

uv pip install --python .venv/bin/python django djangorestframework psycopg2-binary django-htmx


Verify Django:

.venv/bin/python -m django --version   # should print e.g. 5.2.7

6. Create Django project

(If not already created)

django-admin startproject sms .
# creates manage.py and sms/ (settings.py, urls.py, wsgi.py, asgi.py)


Check files:

manage.py
sms/
.venv/


Run initial migrations:

python manage.py migrate


Run server:

python manage.py runserver
# open http://127.0.0.1:8000/ and confirm Django page

7. Apps created so far

You created apps: students, teachers (names matter; plural vs singular must match folders and INSTALLED_APPS)

Create app command (if needed):

python manage.py startapp students
python manage.py startapp teachers


Register each app in sms/settings.py → INSTALLED_APPS:

INSTALLED_APPS = [
    ...,
    'students',
    'teachers',
]

8. Models (examples you added)

students/models.py

from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    class_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    address = models.TextField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"


teachers/models.py

from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    hire_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.subject}"


After editing models:

python manage.py makemigrations
python manage.py migrate

9. Admin registration (so you can add data via /admin)

students/admin.py

from django.contrib import admin
from .models import Student

admin.site.register(Student)


teachers/admin.py

from django.contrib import admin
from .models import Teacher

admin.site.register(Teacher)


Create superuser:

python manage.py createsuperuser
# then visit http://127.0.0.1:8000/admin and login

10. URLs — how they are wired
Main project urls: sms/urls.py

Make sure you import include:

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('students/', include('students.urls')),   # example
    path('teachers/', include('teachers.urls')),
]

App urls (must create urls.py in each app)

students/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_home, name='student_home'),
    path('list/', views.student_list, name='student_list'),
]


teachers/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.teachers, name='teachers'),
    path('list/', views.teacher_list, name='teacher_list'),
]

Example simple view

teachers/views.py

from django.http import HttpResponse
from .models import Teacher
from django.shortcuts import render

def teachers(request):
    return HttpResponse("This is teacher home page")

def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})


Important: don’t include an app’s urls.py inside itself — that causes recursion errors.

11. Templates location

Recommended structure:

teachers/
 └── templates/
      └── teachers/
           └── teacher_list.html
students/
 └── templates/
      └── students/
           └── student_list.html


Django will find templates if APP_DIRS = True in TEMPLATES setting (default).

12. How to view pages in browser

Admin: http://127.0.0.1:8000/admin/

Teachers list (example): http://127.0.0.1:8000/teachers/list/

Teacher home: http://127.0.0.1:8000/teachers/

Students list: http://127.0.0.1:8000/students/list/

If you get 404:

Check sms/urls.py includes the app route

Check app has urls.py and its urlpatterns has the correct view names

Make sure server is running (python manage.py runserver)

13. Common gotchas / troubleshooting

ModuleNotFoundError: No module named 'teachers' → check folder name and INSTALLED_APPS spelling.

RecursionError in URL loading → you included an app’s urls into itself (avoid path('', include('teachers.urls')) inside teachers/urls.py).

404 for /teacher/ vs /teachers/ → check exact path strings (singular/plural).

If Django not found: ensure venv active and packages installed inside that venv.

If VS Code terminal opens as root@... → set WSL default user to your normal user or open WSL as that user.

14. Next recommended steps (what we will do next)

Add templates and style (Tailwind or Bootstrap) for teacher/student list pages.

Add CRUD views and forms for Teacher and Student (Create, Update, Delete).

Add authentication + RBAC: custom User model with role choices (admin, teacher, student, parent).

Add Attendance, Classes, Exams models later (phase-1 MVP plan).

Move to DRF & React later (Phase-2) if you want APIs/mobile app.

15. Useful commands cheat-sheet
# venv
python3 -m venv .venv
source .venv/bin/activate

# install
pip install django djangorestframework psycopg2-binary django-htmx

# project/app
django-admin startproject sms .
python manage.py startapp students
python manage.py startapp teachers

# DB migrations
python manage.py makemigrations
python manage.py migrate

# admin
python manage.py createsuperuser
python manage.py runserver

🧠 Django Project — GitHub Push Guide (with Token)
🔹 1. Initialize Git
git init

🔹 2. Add All Files
git add .

🔹 3. Commit Changes
git commit -m "Initial Django project commit"

🔹 4. Create Main Branch
git branch -M main

🔹 5. Add GitHub Remote Repository
git remote add origin https://github.com/seher873/intial_code_djngo.git

🔐 Set Up GitHub Token (for authentication)

Go to 👉 GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic)

Click "Generate new token (classic)"

Select scopes:

✅ repo

✅ workflow

✅ read:org

Copy the generated token immediately (you won’t see it again).

💻 Use Token While Pushing

When you run:

git push -u origin main


Git will ask:

Username for 'https://github.com': 


➡ Enter your GitHub username (e.g., seher873)

Then it will ask:

Password for 'https://seher873@github.com':


➡ Paste your personal access token instead of your password.

✅ Done!

Now your code will be uploaded to your GitHub repository successfully.
For the next pushes, just run:

git add .
git commit -m "update message"
git push









