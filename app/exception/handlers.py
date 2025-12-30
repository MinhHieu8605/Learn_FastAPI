import traceback
from datetime import datetime

from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

import logging

from Ecommerce.app.schemas.error import ErrorResponse
from Ecommerce.app.exception.http import ResourceNotFoundException
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)


async def resource_not_found_handler(request : Request, exc : ResourceNotFoundException):
    error = ErrorResponse(
        timestamp=datetime.now(),
        status=status.HTTP_404_NOT_FOUND,
        error="Resource Not Found",
        message=exc.message
    )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder(error)
    )

async def validation_exception_handler(request : Request, exc : RequestValidationError):
    error = {
        "timestamp": datetime.now(),
        "status": status.HTTP_400_BAD_REQUEST,
        "error": "Validation Error",
        "message": "Dữ liệu không hợp lệ",
        "details": exc.errors()
    }
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(error)
    )


async def global_exception_handler(
    request: Request,
    exc: Exception
):
    print(f"Error: {exc}")
    print(traceback.format_exc())
    logger.error("Unexpected error", exc_info=exc)
    error = ErrorResponse(
        timestamp=datetime.now(),
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error="An error occurred",
        message=str(exc)
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(error)
    )
