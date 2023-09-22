from django.urls import path

from apps.billing import views

urlpatterns = [
    path(
        "receipts/",
        views.ReceiptsGeneral.as_view(),
        name="receipts_general",
    ),
    path(
        "receipts/<int:id>/",
        views.ReceiptsDetail.as_view(),
        name="receipts_retrieve",
    ),
]
