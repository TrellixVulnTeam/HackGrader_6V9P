import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# ^^^ The above is required if you want to import from the celery
# library.  If you don't have this then `from celery.schedules import`
# becomes `proj.celery.schedules` in Python 2.x since it allows
# for relative imports by default.

# Grader & Docker settings

# In seconds - how long should be wait, before killing docker.
DOCKER_TIME_LIMIT = 5
DOCKER_IMAGE = 'grader'
DOCKER_USER = 'grader'
DOCKER_MEMORY_LIMIT = '300M'
NPROC_SOFT_LIMIT = 49
NPROC_HARD_LIMIT = 49

# Celery settings

BROKER_URL = 'amqp://guest:guest@localhost//'
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-q5gi9t(i%4q9mh@#)672ikx#+_83^6bs2*aqnm8&t+#5=!6z3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
