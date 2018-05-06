import os
from .base import BASE_DIR, config


DATABASES = {}

DATABASE_FILE = os.path.join(BASE_DIR, 'db.sqlite3')

try:
    # https://github.com/kennethreitz/dj-database-url
    import dj_database_url
    DATABASES['default'] = config(
        'DATABASE_URL',
        default='sqlite:///' + DATABASE_FILE,
        cast=dj_database_url.parse,
    )
    if 'mysql' in DATABASES['default']['ENGINE']:
        DATABASES['default']['OPTIONS'] = {'init_command': 'SET names utf8;'}
except ImportError:
    # https://docs.djangoproject.com/en/1.11/ref/settings/#databases
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_FILE,
    }
