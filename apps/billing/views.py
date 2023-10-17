from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.billing.serializers import ProcessTransactionSerializer
from apps.util.base_views import GeneralPost


class ProcessTransaction(APIView, GeneralPost):
    authentication_classes = [TokenAuthentication]
    serializer = ProcessTransactionSerializer
    permission_classes = [IsAuthenticated]
