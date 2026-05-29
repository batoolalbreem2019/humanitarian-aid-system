import os

BASE = os.path.dirname(os.path.abspath(__file__))

SERVICES = [
    {
        "name": "user_service",
        "app": "users",
        "port": "8001",
        "installed": "users",
        "urls": "path('api/users/', include('users.urls')),"
    },
    {
        "name": "aid_request_service",
        "app": "aid_requests",
        "port": "8002",
        "installed": "aid_requests",
        "urls": "path('api/aid-requests/', include('aid_requests.urls')),"
    },
    {
        "name": "donation_service",
        "app": "donations",
        "port": "8003",
        "installed": "donations",
        "urls": "path('api/donations/', include('donations.urls')),"
    },
    {
        "name": "distribution_service",
        "app": "distributions",
        "port": "8004",
        "installed": "distributions",
        "urls": "path('api/distributions/', include('distributions.urls')),"
    },
    {
        "name": "notification_service",
        "app": "notifications",
        "port": "8005",
        "installed": "notifications",
        "urls": "path('api/notifications/', include('notifications.urls')),"
    },
]

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"  ✅ {path.replace(BASE, '')}")

for svc in SERVICES:
    name = svc["name"]
    app  = svc["app"]
    svc_dir = os.path.join(BASE, name)
    pkg_dir = os.path.join(svc_dir, name)

    # ── manage.py
    write(os.path.join(svc_dir, "manage.py"), f'''#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{name}.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django.") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
''')

    # ── package __init__
    write(os.path.join(pkg_dir, "__init__.py"), "")

    # ── settings.py
    write(os.path.join(pkg_dir, "settings.py"), f'''import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-change-in-production')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'rest_framework',
    '{svc["installed"]}',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = '{name}.urls'

TEMPLATES = [{{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {{'context_processors': [
        'django.template.context_processors.request',
    ]}},
}}]

WSGI_APPLICATION = '{name}.wsgi.application'

# Database
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')

if DATABASE_URL.startswith('postgres'):
    import re
    m = re.match(r'postgres://(.+):(.+)@(.+):(\d+)/(.+)', DATABASE_URL)
    if m:
        DATABASES = {{
            'default': {{
                'ENGINE': 'django.db.backends.postgresql',
                'USER':     m.group(1),
                'PASSWORD': m.group(2),
                'HOST':     m.group(3),
                'PORT':     m.group(4),
                'NAME':     m.group(5),
            }}
        }}
    else:
        DATABASES = {{'default': {{'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}}}
else:
    DATABASES = {{'default': {{'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}}}

RABBITMQ_URL = os.environ.get('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')

REST_FRAMEWORK = {{
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
}}

STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_TZ = True
''')

    # ── urls.py
    write(os.path.join(pkg_dir, "urls.py"), f'''from django.urls import path, include

urlpatterns = [
    {svc["urls"]}
]
''')

    # ── wsgi.py
    write(os.path.join(pkg_dir, "wsgi.py"), f'''import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{name}.settings')
application = get_wsgi_application()
''')

    # ── app urls if missing
    app_urls = os.path.join(svc_dir, app, "urls.py")
    if not os.path.exists(app_urls):
        write(app_urls, "from django.urls import path\nurlpatterns = []\n")

    # ── app __init__ if missing
    app_init = os.path.join(svc_dir, app, "__init__.py")
    if not os.path.exists(app_init):
        write(app_init, "")

    print(f"  --- {name} done ---")

# ── notification service extra: add a basic urls.py in notifications
notif_urls = os.path.join(BASE, "notification_service", "notifications", "urls.py")
if not os.path.exists(notif_urls):
    write(notif_urls, '''from django.urls import path
from rest_framework import generics
from .models import Notification
from rest_framework import serializers

class NotifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"

class NotifListView(generics.ListAPIView):
    from .models import Notification as N
    queryset = N.objects.all().order_by('-sent_at')
    serializer_class = NotifSerializer

urlpatterns = [
    path('', NotifListView.as_view()),
]
''')

print("\n✅ All files generated successfully!")
print("\nNow run:")
print("  docker compose up --build")
