from enum import Enum

def includeme(config):
    config.scan('.')

class StatusCodes(Enum):
    DATABASE_ERROR = 1