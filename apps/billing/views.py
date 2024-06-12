import logging

import requests
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.billing.models import Transaction
from apps.billing.serializers import ProcessTransactionSerializer
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
    serializer = ProcessTransactionSerializer
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
    """

    try:
        if not kwargs:
            return Response({"response": "Invalid transaction id"}, status=400)

        transaction = Transaction.objects.get(transaction_id=kwargs["transaction_id"])
        receipt_link = ReceiptDocumentHost().get_document(document_id=transaction.document_id)

        return Response(receipt_link, status=200)
    except requests.exceptions.RequestException as e:
        if e.response.status_code == 404:
            return Response("File not found", status=404)

        return Response("Occurred an error getting the document", status=500)
    except ObjectDoesNotExist:
        return Response("Transaction not found", status=404)
    except Exception:
        log.exception("Not expected error ocurred getting the document")
        return Response("A not expected error ocurred getting the document", status=500)
