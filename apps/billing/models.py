from django.db import models
from django_countries.fields import CountryField

from apps.util.models import BaseModel


class Receipt(BaseModel):
    """
    Represents a receipt issued for a transaction.
    Each receipt contains details about the payer, items in the receipt, and financial information.

    The fields for this model was defined in the following documentation:
        ecommerce_integration_specification
        https://github.com/fccn/nau-financial-manager/blob/main/docs/integrations/ecommerce_integration_specification.md


    - Transaction id
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

    """

    transaction_id = models.CharField(max_length=150, unique=True)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    address_line_1 = models.CharField(max_length=150, null=True, blank=True)
    address_line_2 = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country_code = models.CharField(max_length=50, null=True, blank=True)
    vat_identification_number = models.CharField(max_length=20, null=True, blank=True)
    vat_identification_country = CountryField(max_length=255, null=True)
    total_amount_exclude_vat = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_amount_include_vat = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    currency = models.CharField(max_length=7, default="EUR", null=True, blank=True)

    def __str__(self):
        return self.name


class ReceiptItem(BaseModel):
    """
    One-to-many relationship with ReceiptLine model (related_name='receipt_items').

    The fields for this model was defined in the following documentation:
        ecommerce_integration_specification
        https://github.com/fccn/nau-financial-manager/blob/main/docs/integrations/ecommerce_integration_specification.md

    - Description
    - Quantity
    - Amount excluding VAT
    - Amount including VAT
    - Course id
    - Organization code
    - Course code

    """

    receipt = models.ForeignKey(Receipt, related_name="receipt_items", on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True)
    quantity = models.PositiveIntegerField(default=1, null=True)
    vat_tax = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    amount_exclude_vat = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    amount_include_vat = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    organization_code = models.CharField(max_length=255, null=True)
    course_id = models.CharField(max_length=50, null=True, blank=True)
    course_code = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.description
