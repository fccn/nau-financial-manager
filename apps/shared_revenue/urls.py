from django.urls import path

from apps.shared_revenue import views

urlpatterns = [
    path(
        "revenue-configurations/",
        views.RevenueConfigurationGeneral.as_view(),
        name="revenue_configurations_general",
    ),
    path(
        "revenue-configurations/<int:id>/",
        views.RevenueConfigurationDetail.as_view(),
        name="revenue_configurations_detail",
    ),
    path(
        "share-executions/",
        views.ShareExecutionGeneral.as_view(),
        name="share_executions_general",
    ),
    path(
        "share-executions/<int:id>/",
        views.ShareExecutionDetail.as_view(),
        name="share_executions_detail",
    ),
]
