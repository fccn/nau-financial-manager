import logging
from datetime import datetime

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        data = {"error": {"code": response.status_code, "message": response.data}}
        response.data = data
        response.content_type = "application/json"

    logging.getLogger("nau_financial_manager").error(
        f"time:{datetime.now()}, error: {response.data}, exc: '{exc}', context: {context}"
    )
    return response
