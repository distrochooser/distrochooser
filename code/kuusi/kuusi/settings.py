"""
distrochooser
Copyright (C) 2014-2025  Christoph Müller  <mail@chmr.eu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from pathlib import Path
from os.path import dirname, join

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-lxk@%y9u^e50jvzl0q&2!ud&vwtr-3*t^qgo9f20zniyep-h9x"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "host.docker.internal",
    "localhost"
]

# Application definition

ENABLE_PROFILING = False

INSTALLED_APPS = (["silk"] if ENABLE_PROFILING else []) + [
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "web",
    'corsheaders'
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Distrochooser',
    'DESCRIPTION': 'REST API specification',
    'VERSION': '6.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
}

MIDDLEWARE = (['silk.middleware.SilkyMiddleware'] if ENABLE_PROFILING else []) + [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True


if DEBUG:
    MIDDLEWARE.append('django_cprofile_middleware.middleware.ProfilerMiddleware')
    DJANGO_CPROFILE_MIDDLEWARE_REQUIRE_STAFF = False

ROOT_URLCONF = "kuusi.urls"

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

WSGI_APPLICATION = "kuusi.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

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

# This is only relevant for the admin dashboard (if enabled)
LANGUAGE_CODE = "en-us"

AVAILABLE_LANGUAGES = [
    ("de", "Deutsch"),
    ("en", "English"),
    ("az", "Azerbaijani"),
    ("vi", "Vietnamese"),
    ("tr", "Turkish"),
    ("sv", "Swedish"),
    ("fi", "Finnish"),
    ("pl", "Polnish"),
    ("es", "Spanish"),
    ("nl", "Dutch"),
    ("it", "Italian"),
    ("id", "Indonesian"),
    ("el", "Greek"),
    ("he", "Hebrew"),
    ("ru", "Russian"),
    ("fr", "French"),
    ("pt", "Portuguese"),
    ("gsw", "Swiss German"),
    ("ja", "Japanese"),
    ("zh-hans", "Chinese (simplified)"),
    ("sl", "Slowenian")
]

RTL_LANGUAGES = [
    "he"
]

FRONTEND_URL = "http://localhost:3000"

TIME_ZONE = "UTC"

USE_I18N = False

USE_TZ = True

STATIC_URL = "/static/"

# per default, the /static/ folder is located on the repo root, which is two levels above the BASE_DIR
STATICFILES_DIRS = (join(dirname(dirname(BASE_DIR)), "static"),)

# per default, the /static_root/ folder is located on the repo root and is used as the target for the static files to server
STATIC_ROOT = join(dirname(dirname(BASE_DIR)), "static_root")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# per default, the /locale/ folder is located on the repo root, which is two levels above the BASE_DIR
LOCALE_PATHS = (join(dirname(dirname(BASE_DIR)), "locale"),)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}

KUUSI_URL = "http://localhost:8000"

FRONTEND_URL = "http://localhost:3000"

KUUSI_NAME = "Distrochooser"

DEFAULT_LANGUAGE_CODE = "en"
KUUSI_META_TAGS = {
    "twitter:card": "summary",
    "twitter:title": KUUSI_NAME,
    "twitter:description": "",
    "twitter:image": KUUSI_URL + "/logo.png",
    "og:title": KUUSI_NAME,
    "og:type": "website",
    "og:url": KUUSI_URL,
    "og:image": KUUSI_URL + "/logo.png",
    "og:image:type": "image/png",
    "og:image:width": "100",
    "og:image:height": "100",
    "og:description": "",
    "og:locale": DEFAULT_LANGUAGE_CODE,
    "og:site_name": "Distrochooser",
    "theme-color": "#158cba"
}

SESSION_NUMBER_OFFSET = 1754516

WEIGHT_MAP = {-2: -0.5, -1: -0.25, 0: 1, 1: 2, 2: 4}


KUUSI_LOGO = "http://localhost:8000/static/logo.svg"

KUUSI_ICON = "http://localhost:8000/static/icon.svg"

# Some selected endpoints will create an individual cache to prevent overboarding load times
CACHE_TIMEOUT = 120

LONG_CACHE_TIMEOUT = 60 * 60 * 24 

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": join(dirname(dirname(BASE_DIR)), "cache"),
        "TIMEOUT": CACHE_TIMEOUT,
        "OPTIONS": {"MAX_ENTRIES": 1000},
    }
}

IMPRINT = """
ich
da
dort
bla
"""

PRIVACY = ""

DISCORD_HOOK = ""