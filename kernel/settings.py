"""
Django settings for kernel project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from typing import Dict

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(#&h0%n78n+hyp)nz)4qfa_dm2)gx0c@6h$nq^!8n7jk5l=ck4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'elearning.warehouse'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kernel.urls'


WSGI_APPLICATION = 'kernel.wsgi.application'


# Logging config
import tomllib
import logging.handlers
from logging.config import dictConfig

from painless.utils.funcs import is_path_exist, create_dir


TOML_LOGGING_CONFIG_PATH = BASE_DIR / "config" / "log" / "config.toml"
try:
    with TOML_LOGGING_CONFIG_PATH.open(mode="rb") as log_config_file:
        log_config = tomllib.load(log_config_file)
except FileNotFoundError as error:
    print(f"Error: TOML log configuration file not found at {TOML_LOGGING_CONFIG_PATH}\n")
    raise
except Exception as error:
    print(f"Error loading TOML log configuration: {error}\n")
    raise
else:
    LOGGING_CONFIG = None
    LOGGING = log_config

    # Check or Create the dirs of log files specified in the config.
    handlers: Dict[str, dict] = LOGGING.get("handlers", None)
    for handler in handlers.values():
        handler_file_path = handler.get("filename", None)
        if handler_file_path:
            if not is_path_exist(BASE_DIR / handler_file_path):
                create_dir(BASE_DIR / handler_file_path)

    logging.config.dictConfig(LOGGING)


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "online_university_db_2",
        "USER": "online_university_user2",
        "PASSWORD": "Q-V3dGx8RkKKoMwwHYO06aRglj06_V_p02cE1n7fGYQ",
        "HOST": "127.0.0.1",
        "PORT": "5432",
        "TEST": {
            "NAME": "online_university_db_test4"
        }
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',   # noqa: E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',             # noqa: E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',            # noqa: E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',           # noqa: E501
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/


TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# ############################### #
#            TEMPLATES            #
# ############################### #
TEMPLATE_DIR="media/templates"
TEMPLATES_DIR = os.path.join(BASE_DIR, TEMPLATE_DIR)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'django.templatetags.static',
                'django.templatetags.i18n',
            ]
        },
    },
]

# ############################### #
#             STATIC              #
# ############################### #


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_DIR="media/static"
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, STATIC_DIR),
)

COLLECT_STATIC_DIR="media/collectstatic"
STATIC_ROOT = os.path.join(
    BASE_DIR, COLLECT_STATIC_DIR
)

MEDIA_URL="/media/"

MEDIA_UPLOAD_DIR="media/uploads"
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_UPLOAD_DIR)


# ############################### #
#      INTERNATIONALIZATION       #
# ############################### #

LANGUAGES = [
    ('en-us', 'English'),
    ('fa', 'Persian'),
]

LANGUAGE_CODE = 'en-us'

LOCALE_DIR = "locales"
LOCALE_PATHS = (
        os.path.join(
            BASE_DIR,
            LOCALE_DIR
        ),
    )



# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
