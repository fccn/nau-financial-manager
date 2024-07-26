import logging

import requests
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.billing.models import Transaction
from apps.billing.serializers import ProcessTransactionSerializerForAPI
from apps.billing.services.receipt_host_service import ReceiptDocumentHost
from apps.util.base_views import GeneralPost

log = logging.getLogger(__name__)


class ProcessTransaction(APIView, GeneralPost):
    """
    Process/save Transaction

    Api that creates and processes transactions.
    It's responsible for validating and processing transaction data.

    It uses the Django Rest Framework with a Token Authentication approach,
    meaning that the client should send the `Authorization` HTTP header with a value of `Token`
    string plus the value of the token, example:
        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    authentication_classes = [TokenAuthentication]
    serializer = ProcessTransactionSerializerForAPI
    permission_classes = [IsAuthenticated]


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def get_receipt_link(request, *args, **kwargs):
    """
    Get Receipt Link

    This method is the endpoint method called through `receipt-link/<str:transaction_id>/`.

    It uses the Django Rest Framework with a Token Authentication approach,
    meaning that the client should send the `Authorization` HTTP header with a value of `Token`
    string plus the value of the token, example:
        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a

    Returns a Json with a response.
    - 200
    {"response": "https://ilink.acin.pt/ilinktests-api/file/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
    - 404 - if transaction isn't found or the file is missing on iLink
    - 400 - if transaction if isn't found
    - 500 - if error getting document
    """

    try:
        if not kwargs:
            return Response({"response": "Invalid transaction id"}, status=status.HTTP_400_BAD_REQUEST)

        transaction = Transaction.objects.get(transaction_id=kwargs["transaction_id"])
        receipt_link = ReceiptDocumentHost().get_document(document_id=transaction.document_id)

        return Response({"response": receipt_link}, status=status.HTTP_200_OK)
    except requests.exceptions.RequestException as e:
        if e.response.status_code == status.HTTP_404_NOT_FOUND:
            return Response({"response": "File not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {"response": "Occurred an error getting the document"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except ObjectDoesNotExist:
        return Response({"response": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        log.exception("Not expected error ocurred getting the document")
        return Response(
            {"response": "A not expected error ocurred getting the document"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
