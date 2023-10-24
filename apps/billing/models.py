from django.db import models
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
    country_code = CountryField(max_length=255, null=True)
    vat_identification_number = models.CharField(max_length=20, null=True, blank=True)
    vat_identification_country = CountryField(max_length=255, null=True)
    total_amount_exclude_vat = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_amount_include_vat = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    currency = models.CharField(max_length=7, default="EUR", null=True, blank=True)
    payment_type = models.CharField(max_length=20, null=True, blank=True)
    transaction_type = models.CharField(max_length=15, choices=TRANSACTION_TYPE)
    transaction_date = models.DateTimeField(null=True, blank=True)
    document_id = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.client_name


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

    """

    transaction = models.ForeignKey(Transaction, related_name="transaction_items", on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True)
    quantity = models.PositiveIntegerField(default=1, null=True)
    vat_tax = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    amount_exclude_vat = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    amount_include_vat = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    organization_code = models.CharField(max_length=255, null=True)
    product_id = models.CharField(max_length=50, null=True, blank=True)
    product_code = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.description
