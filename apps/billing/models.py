from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from apps.util.constants import TRANSACTION_TYPE
from apps.util.models import BaseModel


class Transaction(BaseModel):
    """
    Represents a transaction.
    Each transaction contains details about the payer, items in the transaction, and financial information.

    The fields for this model was defined in the following documentation:
        ecommerce_integration_specification
        https://github.com/fccn/nau-financial-manager/blob/main/docs/integrations/ecommerce_integration_specification.md


    - Transaction id
    - Transaction date
    - Transaction type
    - Payment Type
    - Client Name
    - Email
    - Address
        * Address Line 1
        * Address Line 2
        * City
        * Postal Code
        * State
        * Country Code
    - VAT Identification Number
    - VAT Identification Country
    - Total amount excluding VAT
    - Total amount including VAT
    - Currency
    - Document Id

    """

    transaction_id = models.CharField(max_length=150, unique=True)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    address_line_1 = models.CharField(max_length=150, null=True, blank=True)
    address_line_2 = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country_code = CountryField(max_length=255, null=True, blank=True)
    vat_identification_number = models.CharField(max_length=20, null=True, blank=True)
    vat_identification_country = CountryField(max_length=255, null=True, blank=True)
    total_amount_exclude_vat = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount_include_vat = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=7, default="EUR")
    payment_type = models.CharField(max_length=20, default="credit_card")
    transaction_type = models.CharField(max_length=15, choices=TRANSACTION_TYPE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    document_id = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.transaction_id


class TransactionItem(BaseModel):
    """
    One-to-many relationship with Transaction model (related_name='transaction_items').

    The fields for this model was defined in the following documentation:
        ecommerce_integration_specification
        https://github.com/fccn/nau-financial-manager/blob/main/docs/integrations/ecommerce_integration_specification.md

    - Description
    - Quantity
    - Amount excluding VAT
    - Amount including VAT
    - Product id
    - Organization
    - Product code
    - Discount

    """

    transaction = models.ForeignKey(Transaction, related_name="transaction_items", on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    vat_tax = models.DecimalField(max_digits=5, decimal_places=2)
    unit_price_excl_vat = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price_incl_vat = models.DecimalField(max_digits=10, decimal_places=2)
    organization_code = models.CharField(max_length=255)
    product_id = models.CharField(max_length=50)
    product_code = models.CharField(max_length=50)
    discount = models.DecimalField(
        default=0.0,
        max_digits=3,
        validators=[MaxValueValidator(1), MinValueValidator(0)],
        decimal_places=2,
    )

    def __str__(self):
        return self.product_id


class SageX3TransactionInformation(BaseModel):
    """
    Represents the status of a transaction in the Sage X3 system.
    """

    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    STATE_CHOICES = (
        (PENDING, PENDING),
        (SUCCESS, SUCCESS),
        (FAILED, FAILED),
    )

    transaction = models.OneToOneField(
        Transaction, related_name="sage_x3_transaction_information", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=255, null=False, blank=False, choices=STATE_CHOICES, default=PENDING)
    last_status_date = models.DateTimeField(auto_now_add=True)
    retries = models.PositiveIntegerField(default=0)
    series = models.CharField(
        _("Serie"),
        default=getattr(settings, "DEFAULT_SERIES"),
        max_length=50,
        help_text=_("The transaction series, by default we should use FRN, to fix date issues use FRX"),
    )
    input_xml = models.TextField(null=True, blank=True)
    output_xml = models.TextField(null=True, blank=True)
    error_messages = models.TextField(null=True, blank=True)

    @property
    def processor_custom_fields(self):
        d = dict()
        d["series"] = self.series
        return d

    def __str__(self):
        return f"{self.transaction.transaction_id} - {self.status}"
