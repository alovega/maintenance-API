"""
Configuration variable
"""


class Config(object):
    """
    parent configuration class
    """

    DEBUG = False
    TESTING = False


class Development(Config):
    """
    Development configuration class
    """

    DEBUG = True


class Testing(Config):
    """
    Testing configuration class
    """

    TESTING = False
    DEBUG = False


app_config = {
    "development": Development,
    "testing": Testing,
}