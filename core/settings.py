import os
from datetime import timedelta
from sys import path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

path.insert(0, BASE_DIR)
path.insert(0, os.path.join(BASE_DIR, 'apps'))
path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4u^^db@*qdhoy&*sandkr0q_0tu#h4w8&e=+hf6r8+vfk227gu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


AUTH_USER_MODEL = 'user.Users'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'graphene_django',
    'crispy_forms',
    'DjangoUeditor',
    'xadmin',
    'user.apps.UserConfig',
    'menu.apps.MenuConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'graphql_jwt.middleware.JSONWebTokenMiddleware',
    'core.middleware.LoginRequiredMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_graphql',
        'USER': 'root',
        'PASSWORD': '111111',
        'HOST': '127.0.0.1',
        'OPTIONS': {
            'init_command': 'SET default_storage_engine=INNODB;'
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/
# 设置时区

LANGUAGE_CODE = 'zh-hans'  # 中文支持，django1.8以后支持；1.8以前是zh-cn
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False   # 默认是True，时间是utc时间，由于我们要用本地时间，所用手动修改为false！！！！


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = "/media/"

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

GRAPHENE = {
    'SCHEMA': 'core.schema.schema'
}

# https://github.com/flavors/django-graphql-jwt/blob/master/README.rst

# AUTHENTICATION_BACKENDS = [
#     'graphql_jwt.backends.JSONWebTokenBackend',
#     'django.contrib.auth.backends.ModelBackend',
# ]

GRAPHQL_JWT = {
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_EXPIRATION_DELTA': timedelta(minutes=60),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(minutes=30),
}

# APPEND_SLASH = False

# 跨域增加忽略
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = True

# 需要登录才能访问的地址
LOGIN_EXEMPT_URLS = ('graphiql/',)

LOGGING = {
    'disable_existing_loggers': False,
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(module)s:%(funcName)s] [%(levelname)s] - %(message)s'
        },
        'database': {
            'format': '%(asctime)s - %(message)s'
        },
        'error': {
            'format': '%(asctime)s [%(module)s:%(funcName)s] [%(name)s] - %(message)s'
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/info.log',            # 日志输出文件
            'maxBytes': 1024 * 1024 * 5,              # 文件大小
            'backupCount': 2,                         # 备份份数
            'formatter': 'standard',                  # 使用哪种formatters日志格式
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/error.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 2,
            'formatter': 'error',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'database_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/database.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 2,
            'formatter': 'database',
        }
    },
    'loggers': {
        '': {
            'handlers': ['error', 'console'],
            'level': 'ERROR',
            'propagate': False
        },
        'django': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.db': {
            'handlers': ['database_handler', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}
