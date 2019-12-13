import os
from json import load

CONFIG = {}


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(os.path.dirname(BASE_DIR), "distrochooser.json")

with open(CONFIG_PATH, 'r') as f:
    CONFIG = load(f)

SECRET_KEY = CONFIG["backend"]["SECRET_KEY"]
DEBUG = CONFIG["backend"]["DEBUG"]
ALLOWED_HOSTS = CONFIG["backend"]["ALLOWED_HOSTS"]


CACHEOPS_REDIS = CONFIG["backend"]["CACHE"]["CACHEOPS_REDIS"]
CACHEOPS = CONFIG["backend"]["CACHE"]["CACHEOPS"]


INSTALLED_APPS = [
    'cacheops',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'distrochooser.apps.DistrochooserConfig',
    'corsheaders'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = CONFIG["backend"]["DATABASES"]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LOCALES = {}
for key, value in CONFIG["backend"]["LOCALES"].items():
    LOCALES[key] = os.path.join(os.path.join(BASE_DIR, 'locale'), value + ".po")

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

CORS_ORIGIN_ALLOW_ALL = True

CSRF_COOKIE_SECURE = False

MEDIA_ROOT = "media/"
