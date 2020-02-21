"""
Django settings for kidsclub project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qke)dgfjrc6ikp)oon#si-lv1xrn#s-#6alo40=&5dx930_f%)'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    # 'rest_framework.authtoken',
    'sslserver',
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',
    'knox',
    'videoservices',
    'mailapp',
    'smsapp',
    'corsheaders'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.TokenAuthentication',
        'knox.auth.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
     )
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'kidsclub.urls'
CORS_ORIGIN_ALLOW_ALL = True
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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'kidsclub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kids_club_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'banaoapp_kidsclub',
#         'USER': 'banaoapp_kids',
#         'PASSWORD': 'kidsclub@12345',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#         'OPTIONS': {
#             'sql_mode': 'traditional',
#         }
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# AUTHENTICATION_BACKENDS = ('backends.EmailandPhoneAuthBackend', 'django.contrib.auth.backends.ModelBackend',)
AUTHENTICATION_BACKENDS = (
    'backends.EmailandPhoneAuthBackend',
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
)
# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#************The below settings for EMAIL AND SMS SEND IS FOR TEST AND DEVELOPMENT ****************************

#===============Email================================#
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FROM_C = 'shyamdemo2018@gmail.com'
DEFAULT_FROM_EMAIL = 'shyamdemo2018@gmail.com'

'''
    GMAIL Configaration (Demo)
'''
SERVER_EMAIL = 'shyamdemo2018@gmail.com'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'shyamdemo2018@gmail.com'
EMAIL_HOST_PASSWORD = 'hjtrgqurebsusywx'


# ============= SMS configrations =================
SMS_URL = "https://sms.faresms.com/api_v2/message/send"
SMS_API_KEY = "g7B5sc9OU_y1f-f35t8LnfFO2VELyBzRdXATCxljovrfcJjDOI3hZV1XQO1X8zfY"
SMS_PORT = 80
SMS_USER = 'shail'
SMS_PASS = '62009'
SMS_SENDER = 'SSILMA'

######### TEXT LOCAL SMS GATEWAY CONFIGURATION ########

TXT_LOCAL_SMS_API_KEY = "TXjUs8d/J0w-nGlbXJH2yCDthHQ0xh8VDkVlM2Z8Xh"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '')

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads/media')
MEDIA_URL = '/media/'

# ============= Error Msg configrations =================
MSG_SUCCESS="Success"
MSG_NO_DATA="No Data Found"
MSG_ERROR="Failure"
# ============= Error Msg configrations =================

# #=================TESTING AND DEVELOPMENT CONFIGRATION FOR SOCIAL AUTH================================= 
# # Facebook configuration
# SOCIAL_AUTH_FACEBOOK_KEY = ''
# SOCIAL_AUTH_FACEBOOK_SECRET = ''

# # Define SOCIAL_AUTH_FACEBOOK_SCOPE to get extra permissions from Facebook.
# # Email is not sent by default, to get it, you must request the email permission.
# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

# SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {       # add this
#       'fields': 'id, name, email, picture.type(large), link'
#     }
# SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [                 # add this
#         ('name', 'name'),
#         ('email', 'email'),
#         ('picture', 'picture'),
#         ('link', 'profile_url'),
#     ]

# SOCIAL_AUTH_PIPELINE = (
#     'social_core.pipeline.social_auth.social_details',
#     'social_core.pipeline.social_auth.social_uid',
#     'social_core.pipeline.social_auth.auth_allowed',
#     'social_core.pipeline.social_auth.social_user',
#     'social_core.pipeline.social_auth.associate_user',
#     'social_core.pipeline.social_auth.load_extra_data',
#     'social_core.pipeline.user.user_details',
#     # 'users.social_auth_pipeline.create_user_by_type', #custome pipline during the authentication to create user with custome details
# )

#***********************************XXXXXXXX**************************************************************