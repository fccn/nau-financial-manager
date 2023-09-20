from django.db import models
from django_countries.fields import CountryField

from apps.organization.models import Organization
from apps.util.models import BaseModel


class Receipt(BaseModel):
    """
    Represents a receipt issued for a transaction.
    Each receipt contains details about the payer, items in the receipt, and financial information.
    """

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    vat_identification_country = CountryField(max_length=255)
    vat_identification_number = models.CharField(max_length=20)
    total_amount_exclude_vat = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount_include_vat = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_link = models.CharField(max_length=255)
    receipt_document_id = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, related_name="organization_receipts", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ReceiptItem(BaseModel):
    """
    One-to-many relationship with ReceiptLine model (related_name='receipt_items').
    """

    receipt = models.ForeignKey(Receipt, related_name="receipt_items", on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    vat_tax = models.DecimalField(max_digits=5, decimal_places=2)
    amount_exclude_vat = models.DecimalField(max_digits=10, decimal_places=2)
    amount_include_vat = models.DecimalField(max_digits=10, decimal_places=2)
    organization_code = models.CharField(max_length=255)
    course_code = models.CharField(max_length=255)
    course_id = models.CharField(max_length=255)

    def __str__(self):
        return self.description

    class Meta:
        constraints = [models.UniqueConstraint(fields=["receipt"], name="unique_receipt_item")]
