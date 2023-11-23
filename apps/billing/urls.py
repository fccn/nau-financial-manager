from django.urls import path

from apps.billing import views

urlpatterns = [
    path(
        "transaction-complete/",
        views.ProcessTransaction.as_view(),
        name="transaction_complete",
    ),
    path(
        "invoice-link/<str:transaction_id>/",
        views.get_invoice_link,
        name="get_invoice_link",
    ),
]
