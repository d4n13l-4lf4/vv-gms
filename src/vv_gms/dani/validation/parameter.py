from functools import wraps
from typing import Callable, Any


def validate(validators: dict[str, Callable[[Any], None]]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            from inspect import signature
            bound = signature(f).bind(*args, **kwargs)
            bound.apply_defaults()
            for param, validator in validators.items():
                if param in bound.arguments:
                    validator(bound.arguments[param])
            return f(*args, **kwargs)
        return wrapper
    return decorator