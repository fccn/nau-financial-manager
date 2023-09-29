from uuid import uuid4

from django.db import models
from django_countries.fields import CountryField

from apps.organization.models import Organization
from apps.util.models import BaseModel


class Product(BaseModel):

    """
    This model that represents the bought product
    Each ReceiptItem is a product, item price is the product price
    """

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="product_organization", null=True, blank=True
    )
    product_id = models.CharField(max_length=100, null=True, blank=True)


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

    # The uuid field will be the pair identification with the transaction_id saved in the ecommerce
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    transaction_id = models.CharField(max_length=150, null=True, unique=True)
    client_name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    address_line_1 = models.CharField(max_length=150, null=True)
    address_line_2 = models.CharField(max_length=150, null=True)
    city = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    country_code = models.CharField(max_length=50, null=True)
    vat_identification_number = models.CharField(max_length=20, null=True)
    vat_identification_country = CountryField(max_length=255, null=True)
    total_amount_exclude_vat = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_amount_include_vat = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    currency = models.CharField(max_length=7, default="EUR", null=True)

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="item_product", null=True, blank=True)

    def __str__(self):
        return self.description
