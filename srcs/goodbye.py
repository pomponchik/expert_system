from srcs.settings import settings
from srcs.errors import InternalError


def goodbye(message):
    if settings['interactive']:
        raise InternalError(message)
    else:
        print(message)
        exit(1)
