from django.urls import path

from apps.billing import views

urlpatterns = [
    path(
        "receipt-complete/",
        views.ProcessTransaction.as_view(),
        name="receipt_complete",
    ),
]
