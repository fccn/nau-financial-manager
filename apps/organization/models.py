from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from apps.util.constants import ADDRESS_TYPES, CONTACT_TYPES
from apps.util.models import BaseModel


class Organization(BaseModel):
    """
    A model representing an organization.
    """

    uuid = models.UUIDField(_("Uuid"), primary_key=True, default=uuid4, editable=False, db_index=True)
    name = models.CharField(_("Name"), max_length=255)
    short_name = models.CharField(_("Short Name"), max_length=50, db_index=True)
    slug = models.SlugField(_("Slug"), max_length=50, db_index=True, unique=True)
    vat_country = CountryField()
    vat_number = models.CharField(_("Vat Number"), max_length=50, unique=True)
    iban = models.CharField(_("Iban"), max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    def __str__(self) -> str:
        return self.name


class OrganizationAddress(BaseModel):
    """
    A model representing an address for an organization.
    """

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="organization_addresses")
    address_type = models.CharField(_("Address Type"), max_length=11, choices=ADDRESS_TYPES, default="home")
    street = models.CharField(_("Street"), max_length=150, null=True)
    postal_code = models.DecimalField(_("Postal Code"), max_digits=7, decimal_places=0, null=True)
    city = models.CharField(_("City"), max_length=50, null=True)
    district = models.CharField(_("District"), max_length=50, null=True)
    country = CountryField(default="PT")

    class Meta:
        verbose_name = _("Organization address")
        verbose_name_plural = _("Organizations addresses")

    def __str__(self) -> str:
        return f"{self.organization.name} - {self.address_type}"


class OrganizationContact(BaseModel):
    """
    A model representing a contact for an organization.
    """

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="organization_contacts")
    contact_type = models.CharField(_("Contact Type"), max_length=6, choices=CONTACT_TYPES, null=False)
    contact_value = models.CharField(_("Contact Value"), max_length=50, null=False)
    description = models.CharField(_("Description"), max_length=255, null=True, blank=True)
    is_main = models.BooleanField(_("Is Main"), default=False)

    class Meta:
        verbose_name = "Organization contact"
        verbose_name_plural = "Organizations contacts"
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "contact_type"],
                condition=models.Q(is_main=True, deleted__isnull=True),
                name="unique_main_contact_per_type",
            )
        ]

    def __str__(self) -> str:
        return f"{self.organization.name} - {self.contact_type}"
