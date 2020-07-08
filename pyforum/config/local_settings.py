# flake8: noqa

import logging

from .settings import *  # noqa

# ==============================================================================
# CORE SETTINGS
# ==============================================================================

INSTALLED_APPS += [  # noqa
    'debug_toolbar',
]


# ==============================================================================
# MIDDLEWARE SETTINGS
# ==============================================================================

DEBUG_MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',

]

MIDDLEWARE = DEBUG_MIDDLEWARE + MIDDLEWARE   # noqa
