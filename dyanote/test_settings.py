# Django settings for dyanote project.

import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

USE_TZ = True

SITE_ID = 2

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(PROJECT_ROOT), "client", "app"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'r8&2%r7-nzx!alr&pvlji)*4afps^o3_grkh=%x3i0e^1+1sh)'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'dyanote.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'dyanote.wsgi.application'


INSTALLED_APPS = (
    # Local apps
    'api',

    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Enable admin interface.
    'django.contrib.admin',

    # We use Django Rest Framework for our REST api.
    'rest_framework',
    # We use OAuth2 for authentication
    'provider',
    'provider.oauth2',
    # Add CORS headers
    'corsheaders'
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.OAuth2Authentication',
    )
}
