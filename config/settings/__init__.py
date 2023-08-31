from .base import *
# import os


environtment = env.str('ENVIRONMENT', 'dev')
DEBUG = env.bool('DEBUG', False)
SECRET_KEY=env.str('SECRET_KEY')
ALLOWED_HOSTS = env.str('ALLOWED_HOSTS').split(' ')


if environtment == 'production':
    from .prod import *

elif environtment == 'development':
    # INSTALLED_APPS += [
    #     'debug_toolbar',
    # ]
    from .local import *


