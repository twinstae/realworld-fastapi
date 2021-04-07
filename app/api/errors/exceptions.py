from fastapi import HTTPException
from starlette import status


def HTTP_400_BAD_REQUEST_Exception(detail: str):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail
    )
