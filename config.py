# encoding: utf-8

class BaseConfig(object):
    ENABLED_MODULES = {
        'api',
    }

    SWAGGER_UI_JSONEDITOR = True


class DevelopmentConfig(BaseConfig):
    """config for DevelopmentConfig."""
    DEBUG = True
    DEVELOPMENT = True