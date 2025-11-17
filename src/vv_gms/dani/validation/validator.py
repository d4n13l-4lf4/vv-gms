import decimal
from typing import Any

from vv_gms.dani.exception.custom import CustomException


def between(min_val: int | float, max_val: int | float, inclusive: bool, error_msg: str):
    def __inner__(data: Any):
        try:
            decimal_value = decimal.Decimal(data)
            if inclusive and not min_val <= decimal_value <= max_val:
                raise CustomException(error_msg)
            if not inclusive and not min_val < decimal_value < max_val:
                raise CustomException(error_msg)
        except Exception:
            raise  CustomException(error_msg)
    return __inner__

def not_empty(err_msg: str):
    def __inner__(data: Any):
        # safe check for data as str
        if data is None or len(data.strip()) == 0:
            raise CustomException(err_msg)
    return __inner__