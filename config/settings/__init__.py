from .base import *
# import os
import environs

env = environs.Env()
env.read_env()

environtment = env('ENVIRONMENT', 'local')


if environtment == 'production':
    from .prod import *

elif environtment == 'local':
    # INSTALLED_APPS += [
    #     'debug_toolbar',
    # ]
    from .local import *


