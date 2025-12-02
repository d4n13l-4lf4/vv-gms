import json
from decimal import ROUND_HALF_UP, Decimal
from functools import wraps

from vv_gms.shared import load_data, save_data


def sync_file():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = load_data()
            result = f(*args, **kwargs, data=data)
            save_data(data)
            return result
        return wrapper
    return decorator