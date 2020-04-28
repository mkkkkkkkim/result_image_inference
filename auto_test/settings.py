"""
Django settings for auto_test project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hw*i--86=9+%4fm0@k1saxzytc7j2qrff$*$jv2^7b7@t5*e5^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'image_test',
    'django_crontab',    # Django crontab
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'auto_test.urls'

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

WSGI_APPLICATION = 'auto_test.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    # MySQL 연결
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'extest2',    # DB name
        'USER': 'guser',
        'PASSWORD': 'tomatoSWEte@m',
        'HOST': '211.109.22.29',
        'PORT': '3306'
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

'''
- LOGGING settings
    - 파일에 저장하는 로거와 콘솔에 출력하는 로거 2개 생성
    - 사용하기 위해서는
        import logging
        logger = logging.getLogger(__name__)
        logger.debug('this is log info')
        - __name__ 은 로거를 호출한 파일의 파일명이 됨
    - level : debug, info, warning, error, critical
'''
LOGGING = {
    'version': 1,
    # 기존의 로깅 설정을 비활성화 할 것인가?
    'disable_existing_loggers': False,

    # formatter
    # 로그 레코드는 최종적으로 텍스트로 표현됨
    # 이 텍스트의 포맷 형식 정의
    # 여러 포맷 정의 가능
    'formatters': {
        'format': {
            # [접근시간] 로그레벨 [로그이름 라인넘버] 로그메세지
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        }
    },

    # handler
    # 로그 레코드로 무슨 작업을 할 것인지 정의
    # 여러 핸들러 정의 가능
    'handlers': {
        # 콘솔(터미널)에 출력
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'format',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'format',
            'filename': 'debug.log',
        }
    },

    # logger
    # 로그 레코드 저장소
    # 로거를 이름별로 정의
    # 현재는 로그를 DEBUG 수준 이상의 모든 메세지를 출력
    'loggers': {
        'image_test': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        }
    },
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_TZ = False
TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/meida/'
# TODO : 루트 디렉토리 경로 설정
MEDIA_ROOT = '/Users/image'
MODEL_ROOT = os.path.join(MEDIA_ROOT, 'ai_models')
IMAGE_ROOT = os.path.join(MEDIA_ROOT, 'image')

'''
- 인공지능과 관련된 공통된 변수
'''

# 한번만 로드하는 모델 목록
# 공통으로 사용되는 모델
from tensorflow.keras.applications import ResNet152V2, ResNet50
import time
import logging
start = time.time()
RESNET152V2 = ResNet152V2(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)
RESNET152V2.trainable=False

RESNET50 = ResNet50(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)
RESNET50.trainable=False

print('* RESNET init model time :', time.time() - start)

# 성공/실패를 구분하는 기준
# PREDICTION_RATE 보다 크면 성공, 작으면 실패
PREDICTION_RATE = 0.50

# 학습, 테스트 분리 비율
SPLIT_RATIO = 0.2

# 이미지 로드할 때 너비, 높이, 채널
W = 224
H = 224
C = 5


# Crontab OPTIONS
# 실제 os의 crontab에 연결되어 동작하도록 설계되어있음
# python manage.py crontab add 명령어까지 수행해야지 정상 동작 가능함
CRONJOBS = [
    ('* * * * *', 'image_test.cron.test_cron', '>> ' + os.path.join(MEDIA_ROOT, 'tmp.log')),
]
