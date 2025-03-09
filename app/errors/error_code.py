from enum import Enum

from fastapi import status


class ErrorCode(Enum):
    UNKNOWN = -1


def to_http_status_code(error_code: ErrorCode):
    error_code_status_map = {}
    return error_code_status_map.get(
        error_code, status.HTTP_500_INTERNAL_SERVER_ERROR
    )
