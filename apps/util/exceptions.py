from rest_framework import status as http_status
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    try:
        modules = {"Type": exc.detail["message"].code}
        data = {
            "error": {"code": modules["Type"], "message": exc.detail["message"]},
        }
        return Response(data, status=exc.detail["message"].code)
    except Exception as e:
        print(e)
        return Response(
            data={"error": str(exc), "code": 0000, "message": "Code not found, implement..."},
            status=http_status.HTTP_400_BAD_REQUEST,
        )
