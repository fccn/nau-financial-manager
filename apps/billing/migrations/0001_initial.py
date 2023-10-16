# Generated by Django 4.2.5 on 2023-10-13 09:51

import django.db.models.deletion
import django_countries.fields
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
                ("transaction_id", models.CharField(max_length=150, unique=True)),
                ("client_name", models.CharField(blank=True, max_length=255, null=True)),
                ("email", models.CharField(blank=True, max_length=255, null=True)),
                ("address_line_1", models.CharField(blank=True, max_length=150, null=True)),
                ("address_line_2", models.CharField(blank=True, max_length=150, null=True)),
                ("city", models.CharField(blank=True, max_length=100, null=True)),
                ("postal_code", models.CharField(blank=True, max_length=50, null=True)),
                ("state", models.CharField(blank=True, max_length=50, null=True)),
                ("country_code", models.CharField(blank=True, max_length=50, null=True)),
                ("vat_identification_number", models.CharField(blank=True, max_length=20, null=True)),
                ("vat_identification_country", django_countries.fields.CountryField(max_length=255, null=True)),
                ("total_amount_exclude_vat", models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ("total_amount_include_vat", models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ("currency", models.CharField(blank=True, default="EUR", max_length=7, null=True)),
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
                ("description", models.CharField(max_length=255, null=True)),
                ("quantity", models.PositiveIntegerField(default=1, null=True)),
                ("vat_tax", models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ("amount_exclude_vat", models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ("amount_include_vat", models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ("organization_code", models.CharField(max_length=255, null=True)),
                ("course_id", models.CharField(blank=True, max_length=50, null=True)),
                ("course_code", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "receipt",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="receipt_items", to="billing.receipt"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
