from django.urls import path

from apps.organization.views import (
    CompleteOrganizationView,
    OrganizationAddressDetail,
    OrganizationAddressGeneral,
    OrganizationContactDetail,
    OrganizationContactGeneral,
    OrganizationDetail,
    OrganizationGeneral,
)

urlpatterns = [
    path("organizations/", OrganizationGeneral.as_view(), name="organizations_general"),
    path("organizations/<str:slug>/", OrganizationDetail.as_view(), name="organizations_detail"),
    path("addresses/", OrganizationAddressGeneral.as_view(), name="addresses_general"),
    path("addresses/<int:id>/", OrganizationAddressDetail.as_view(), name="addresses_detail"),
    path("contacts/", OrganizationContactGeneral.as_view(), name="contacts_general"),
    path("contacts/<int:id>/", OrganizationContactDetail.as_view(), name="contacts_detail"),
    path("complete-organization/", CompleteOrganizationView.as_view(), name="complete_organization"),
]
