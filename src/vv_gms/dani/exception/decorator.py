import os
from functools import wraps

from vv_gms.dani.exception.custom import CustomException

def catch_error(echoer):
    def __inner__(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except CustomException as e:
                echoer(f"{e}" + os.linesep)
        return wrapper
    return __inner__