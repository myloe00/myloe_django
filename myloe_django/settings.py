import logging
import os.path
import json
from pathlib import Path
from .config.db import DATABASES
from .config.logging import LOGGING


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-%3+)mf*gy(08d2gax3!vf9=!tsfc^9@u2apvs-lu885ebachz3'


DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'rest_framework',
    'django_filters',
    'system',
    'common',
]


# STATIC_URL = 'static/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.ExceptionMiddleware',
    'system.middleware.AuthenticationMiddleware',
    'common.easy_curd.middleware.InterceptPagingRequest',
]

ROOT_URLCONF = 'myloe_django.urls'

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

WSGI_APPLICATION = 'myloe_django.wsgi.application'

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
TOKEN_EXPIRED_TIME = 3600
# 日志配置

RESOURCES_FILE = os.path.join(BASE_DIR, "resources")

# 加载中英
LOCALE_FILE = os.path.join(RESOURCES_FILE, 'locale')
LOCALE = dict()
for file in os.listdir(LOCALE_FILE):
    with open(os.path.join(LOCALE_FILE, file), encoding='utf-8') as f:
        result = json.load(f)
        LOCALE[file.rstrip(".json")] = result

