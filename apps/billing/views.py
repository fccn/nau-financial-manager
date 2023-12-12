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


class ProcessTransaction(APIView, GeneralPost):
    authentication_classes = [TokenAuthentication]
    serializer = ProcessTransactionSerializer
    permission_classes = [IsAuthenticated]


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def get_receipt_link(request, *args, **kwargs):
    """
    This method is the endpoint method called through `receipt-link/<str:transaction_id>/`.
    """

    try:
        if not kwargs:
            return Response({"response": "Invalid transaction id"}, status=400)

        transaction = None
        try:
            transaction = Transaction.objects.get(transaction_id=kwargs["transaction_id"])
        except ObjectDoesNotExist:
            return Response({"response": "Trasaction not found"}, status=404)

        receipt_link = ReceiptDocumentHost().get_document(document_id=transaction.document_id)

        return Response({"response": receipt_link}, status=200)
    except Exception as e:
        raise e
