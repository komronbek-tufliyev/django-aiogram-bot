from .base import *
# import os


environtment = env.str('ENVIRONMENT', 'dev')
DEBUG = env.bool('DEBUG', False)
SECRET_KEY=env.str('SECRET_KEY')
ALLOWED_HOSTS = env.str('ALLOWED_HOSTS').split(' ')


if environtment == 'production':
    from .prod import *

elif environtment == 'development':
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    #~~~~~~~ DJANGO DEBUG TOOLBAR SETTINGS ~~~~~~~#
    INTERNAL_IPS = ['127.0.0.1', '::1']
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
    }
    from .local import *


