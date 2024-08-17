"""
kuusi
Copyright (C) 2014-2024  Christoph Müller  <mail@chmr.eu>

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


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-lxk@%y9u^e50jvzl0q&2!ud&vwtr-3*t^qgo9f20zniyep-h9x"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "crispy_bootstrap5",
    "django.contrib.humanize",
    "web",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "web.middleware.cors.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware"
]

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


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

LANGUAGES = [
    ("en", "en"),
    ("fr","fr"),
    ("nl","nl"),
    ("gr","gr"),
    ("sv","sv"),
    ("tr","tr"),
    ("vn","vn"),
    ("zh-hans","zh-hans"),
    ("it","it"),
    ("es","es"),
    ("de","de"),
    ("pt-br","pt-br"),
    ("gsw","gsw"),
    ("he","he"),
    ("id","id"),
    ("az","az"),
    ("pl","pl"),
    ("zh-hant","zh-hant"),
    ("ru","ru"),
    ("fi","fi"),
]

LANGUAGE_CODES = {
    "en": "en",
    "fr": "fr",
    "nl": "nl",
    "gr": "gr",
    "sv": "sv",
    "tr": "tr",
    "vn": "vn",
    "zh-hans": "zh-hans",
    "it": "it",
    "es": "es",
    "de": "de",
    "pt-br": "pt-br",
    "gsw": "gsw",
    "he": "he",
    "id": "id",
    "az": "az",
    "pl": "pl",
    "zh-hant": "zh-hant",
    "ru": "ru",
    "fi": "fi"
}
TIME_ZONE = "UTC"

USE_I18N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = ("/Users/chm/Documents/distrochooser/static",)

STATIC_ROOT = ""

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOCALE_PATHS = ("/Users/chm/Documents/distrochooser/locale",)

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

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

KUUSI_URL = "http://localhost:8000"

KUUSI_NAME = "Distrochooser"

KUUSI_COPYRIGHT_STRING = None

KUUSI_INFO_STRING = "Made by <a href='https://chmr.eu'>chmr.eu</a>"

KUUSI_TRANSLATION_URL = "https://translate.distrochooser.de"

KUUSI_META_TAGS = {
    "twitter:card": "summary",
    "twitter:title": "Distrochooser",
    "twitter:description": "",
    "twitter:image": KUUSI_URL + "/static/logo.png",
    "og:title": "Distrochooser",
    "og:type": "website",
    "og:url": KUUSI_URL,
    "og:image": KUUSI_URL + "/static/logo.png",
    "og:description": "",
    "theme-color": "#158cba"
}

# use https://turbo.hotwired.dev to prevent flicker
# requires the status codes to be altered.
ACCELERATION = False

SESSION_NUMBER_OFFSET = 1754516

WEIGHT_MAP = {-2: -0.5, -1: -0.25, 0: 1, 1: 2, 2: 4}

DEFAULT_LANGUAGE_CODE = "en"

UPDATE_API_KEY = "fooooooo"

UPDATE_UPLOAD_PATH = "/Users/chm/Documents/distrochooser/tmp"

# Privacy related settings.

# We won't touch the CSRF_COOKIE_AGE because of the reasons mentioned in https://docs.djangoproject.com/en/5.0/ref/settings/#csrf-cookie-age

SESSION_EXPIRE_AT_BROWSER_CLOSE = True # The cookie is not really used for anything rather than picking up data between requests. After the session, it should not be valid anymore

# Forbid certain page from crawling using the robots.txt standard.
# If a rule contains language_code, it will be applied multiple times for all available LANGUAGE_CODES
ROBOTS_TXT = {
    "*": [
        "/language_code/contact",
        "/language_code/privacy"
    ]
}

SITEMAP_PUBLIC_URL = "http://localhost:8000" # please no trailing slash
SITEMAP_ADDITIONAL_ENTRIES = [
    "/language_code/about"
]