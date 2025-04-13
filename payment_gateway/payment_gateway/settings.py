from pathlib import Path
from dotenv import load_dotenv
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

ADYEN_API_KEY = os.getenv('ADYEN_API_KEY')
ADYEN_MERCHANT_ACCOUNT = os.getenv('ADYEN_MERCHANT_ACCOUNT')
ADYEN_CLIENT_KEY = os.getenv('ADYEN_CLIENT_KEY')
ADYEN_PUBLIC_KEY = os.getenv('ADYEN_PUBLIC_KEY')
ADYEN_ENVIRONMENT = os.getenv('ADYEN_ENVIRONMENT', 'Test')
ADYEN_UI_COMPONENT_SOURCE_TEST = os.getenv('ADYEN_UI_COMPONENT_SOURCE_TEST')
ADYEN_UI_COMPONENT_SOURCE_LIVE = os.getenv('ADYEN_UI_COMPONENT_SOURCE_LIVE')
PAYMENT_GATEWAY = os.getenv('PAYMENT_GATEWAY', 'Adyen')

# settings.py

ADYEN_SETTINGS = {
    'API_KEY': 'your_api_key_here',
    'MERCHANT_ACCOUNT': 'your_merchant_account_here',
    'CLIENT_KEY': 'your_client_key_here',
    'PUBLIC_KEY': 'your_public_key_here',
    'ENVIRONMENT': 'Test',  # Can be 'Test' or 'Live'
    'UI_COMPONENT_SOURCE_TEST': 'your_test_ui_component_source',
    'UI_COMPONENT_SOURCE_LIVE': 'your_live_ui_component_source',
}

# Function to get UI component source based on the environment
def get_adyen_ui_component_source():
    environment = ADYEN_SETTINGS['ENVIRONMENT']
    if environment == 'Live':
        return ADYEN_SETTINGS['UI_COMPONENT_SOURCE_LIVE']
    return ADYEN_SETTINGS['UI_COMPONENT_SOURCE_TEST']




SECRET_KEY = 'django-insecure-108!l786lm4ugti3b%qfb6=ou-+y58&v-7d0z7fa$1em%@&v+p'

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'payments',
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

ROOT_URLCONF = 'payment_gateway.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'payment_gateway.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
