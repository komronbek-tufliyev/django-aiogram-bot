from .base import *
# import os


environtment = env.str('ENVIRONMENT', 'dev')


if environtment == 'production':
    from .prod import *

elif environtment == 'development':
    # INSTALLED_APPS += [
    #     'debug_toolbar',
    # ]
    from .local import *


