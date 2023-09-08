# Generated by Django 4.2.4 on 2023-09-08 15:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Receipt",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(db_index=True, editable=False, null=True)),
                ("deleted_by_cascade", models.BooleanField(default=False, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=255)),
                ("address", models.CharField(max_length=255)),
                ("vat_identification_country", models.CharField(max_length=255)),
                ("vat_identification_number", models.CharField(max_length=20)),
                ("total_amount_exclude_vat", models.DecimalField(decimal_places=2, max_digits=10)),
                ("total_amount_include_vat", models.DecimalField(decimal_places=2, max_digits=10)),
                ("receipt_link", models.CharField(max_length=255)),
                ("receipt_document_id", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ReceiptItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(db_index=True, editable=False, null=True)),
                ("deleted_by_cascade", models.BooleanField(default=False, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("description", models.CharField(max_length=255)),
                ("quantity", models.PositiveIntegerField(default=1)),
                ("vat_tax", models.DecimalField(decimal_places=2, max_digits=5)),
                ("amount_exclude_vat", models.DecimalField(decimal_places=2, max_digits=10)),
                ("amount_include_vat", models.DecimalField(decimal_places=2, max_digits=10)),
                ("organization_code", models.CharField(max_length=255)),
                ("course_code", models.CharField(max_length=255)),
                ("course_id", models.CharField(max_length=255)),
                (
                    "receipt",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="receipt_items", to="billing.receipt"
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="receiptitem",
            constraint=models.UniqueConstraint(fields=("receipt",), name="unique_receipt_item"),
        ),
    ]
