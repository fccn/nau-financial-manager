from django.urls import path

from apps.organization.views import OrganizationDetail, OrganizationGeneral

urlpatterns = [
    path("organizations/", OrganizationGeneral.as_view(), name="organizations_general"),
    path("organizations/<str:short_name>/", OrganizationDetail.as_view(), name="organizations_detail"),
]
