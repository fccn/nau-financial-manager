from django.urls import path

from apps.billing import views

urlpatterns = [
    path(
        "transaction-complete/",
        views.ProcessTransaction.as_view(),
        name="transaction_complete",
    ),
]
