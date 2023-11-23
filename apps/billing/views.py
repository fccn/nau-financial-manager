from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from services.document_host_service import InvoiceDocumentHost

from apps.billing.models import Transaction
from apps.billing.serializers import ProcessTransactionSerializer
from apps.util.base_views import GeneralPost


class ProcessTransaction(APIView, GeneralPost):
    authentication_classes = [TokenAuthentication]
    serializer = ProcessTransactionSerializer
    permission_classes = [IsAuthenticated]


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def get_invoice_link(request, *args, **kwargs):
    try:
        if not kwargs:
            return Response({"response": "Invalid transaction id"}, status=400)

        transaction = None
        try:
            transaction = Transaction.objects.get(transaction_id=kwargs["transaction_id"])
        except ObjectDoesNotExist:
            return Response({"response": "Trasaction not found"}, status=404)

        invoice_link = InvoiceDocumentHost().get_document(document_id=transaction.document_id)

        return Response({"response": invoice_link}, status=200)
    except Exception as e:
        raise e
