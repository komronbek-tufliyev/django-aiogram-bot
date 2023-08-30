from .base import BASE_DIR

DATABASES = {
    # amazon s3 bucket
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "",
        'USER': "",
        'PASSWORD': "",
        'HOST': "",
        'PORT': "",
    }
}