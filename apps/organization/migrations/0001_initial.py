# Generated by Django 4.2.4 on 2023-10-04 16:11

import django.db.models.deletion
import django_countries.fields
from django.db import migrations, models

import apps.util.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Organization",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(db_index=True, editable=False, null=True)),
                ("deleted_by_cascade", models.BooleanField(default=False, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=255, null=True, verbose_name="Name")),
                (
                    "short_name",
                    models.CharField(db_index=True, max_length=50, null=True, unique=True, verbose_name="Short Name"),
                ),
                ("vat_country", django_countries.fields.CountryField(max_length=2, null=True)),
                ("vat_number", models.CharField(max_length=50, null=True, unique=True, verbose_name="Vat Number")),
                ("iban", models.CharField(blank=True, max_length=50, null=True, verbose_name="Iban")),
            ],
            options={
                "verbose_name": "Organization",
                "verbose_name_plural": "Organizations",
            },
        ),
        migrations.CreateModel(
            name="OrganizationContact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(db_index=True, editable=False, null=True)),
                ("deleted_by_cascade", models.BooleanField(default=False, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "contact_type",
                    models.CharField(
                        choices=[("email", "Email"), ("phone", "Phone"), ("mobile", "Mobile")],
                        max_length=6,
                        verbose_name="Contact Type",
                    ),
                ),
                (
                    "contact_value",
                    models.CharField(
                        max_length=50,
                        validators=[apps.util.validators.validate_contact_value],
                        verbose_name="Contact Value",
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=255, null=True, verbose_name="Description")),
                ("is_main", models.BooleanField(default=False, verbose_name="Is Main")),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="organization_contacts",
                        to="organization.organization",
                    ),
                ),
            ],
            options={
                "verbose_name": "Organization contact",
                "verbose_name_plural": "Organizations contacts",
            },
        ),
        migrations.CreateModel(
            name="OrganizationAddress",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(db_index=True, editable=False, null=True)),
                ("deleted_by_cascade", models.BooleanField(default=False, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "address_type",
                    models.CharField(
                        choices=[("home", "Home"), ("billing", "Billing"), ("alternative", "Alternative")],
                        default="home",
                        max_length=11,
                        verbose_name="Address Type",
                    ),
                ),
                ("street", models.CharField(max_length=150, null=True, verbose_name="Street")),
                (
                    "postal_code",
                    models.DecimalField(decimal_places=0, max_digits=7, null=True, verbose_name="Postal Code"),
                ),
                ("city", models.CharField(max_length=50, null=True, verbose_name="City")),
                ("district", models.CharField(max_length=50, null=True, verbose_name="District")),
                ("country", django_countries.fields.CountryField(default="PT", max_length=2)),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="organization_addresses",
                        to="organization.organization",
                    ),
                ),
            ],
            options={
                "verbose_name": "Organization address",
                "verbose_name_plural": "Organizations addresses",
            },
        ),
        migrations.AddConstraint(
            model_name="organizationcontact",
            constraint=models.UniqueConstraint(
                condition=models.Q(("deleted__isnull", True), ("is_main", True)),
                fields=("organization", "contact_type"),
                name="unique_main_contact_per_type",
            ),
        ),
    ]
