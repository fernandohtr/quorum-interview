from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "django-insecure-4!7(7fw#f#lpnxs7ybgriu%0k_09p921nvnkr(lxg6x!0r86pt"
DEBUG = True
ALLOWED_HOSTS = []
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = []
LOCAL_APPS = [
    "congress",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
MIDDLEWARE = []
ROOT_URLCONF = "config.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = "config.wsgi.application"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_TZ = True
STATIC_URL = "/staticfiles/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
