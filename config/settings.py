""""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

from environs import Env

env = Env()
env.read_env(
    ".secrets.env", recurse=False
)  # Secrets for dev (external services) not to be put in VC
# The first file loaded takes precedence
env.read_env(".env", recurse=False)  # Default dev environmental variables in VC
# Otherwise, in production, no .env file loaded, and only the environment is used for variables

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("DJANGO_SECRET")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
ENVIRONMENT = env.str("ENVIRONMENT")
if ENVIRONMENT not in ("prod", "dev"):
    raise ValueError(f"ENVIRONMENT: {ENVIRONMENT}, is a wrong value!")

if ENVIRONMENT == "dev":
    from rich import pretty, traceback

    pretty.install()
    traceback.install(show_locals=True)


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # Needed for django-allauth
]

THIRD_PARTY_APPS = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.discord",
    "allauth.socialaccount.providers.steam",
    "django_extensions",
]

PROJECT_APPS = ["profiles"]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [os.path.join(BASE_DIR, "templates_jinja")],
        "APP_DIRS": True,
        "OPTIONS": {"environment": "config.jinja2.environment"},
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates_django")],
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


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB_NAME"),
        "USER": env.str("POSTGRES_DB_USER"),
        "PASSWORD": env.str("POSTGRES_DB_PASSWORD"),
        "HOST": env.str("POSTGRES_HOST"),
        "PORT": env.str("POSTGRES_PORT"),
        "OPTIONS": {"sslmode": env.str("POSTGRES_DB_SSLMODE")},
        "CONN_MAX_AGE": 600,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
TIME_ZONE = env.str("DJANGO_TIMEZONE")

USE_I18N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Default page redirects

LOGIN_REDIRECT_URL = "/"

LOGIN_URL = "/discord/login/"

LOGOUT_REDIRECT_URL = "/"

# Django AllAuth
# https://django-allauth.readthedocs.io/en/latest/overview.html

SITE_ID = 1
# We don't want to allow signing up with email
ACCOUNT_EMAIL_REQUIRED = False
AUTH_USER_MODEL = "profiles.Profile"
SOCIALACCOUNT_PROVIDERS = {
    "discord": {
        "APP": {
            "client_id": env.str("DISCORD_OAUTH_CLIENT_ID"),
            "secret": env.str("DISCORD_OAUTH_CLIENT_SECRET"),
        }
    }
}
ACCOUNT_TEMPLATE_EXTENSION = "j2"

DISCORD_BOOTSTRAP_ADMIN_UID = env.str("DISCORD_BOOTSTRAP_ADMIN_UID", default=None)
