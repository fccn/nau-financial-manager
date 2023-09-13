# Generated by Django 4.2.4 on 2023-09-08 15:35

import uuid

import django.db.models.deletion
from django.db import migrations, models

import apps.util.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Organization",
            fields=[
                ("deleted", models.DateTimeField(db_index=True, editable=False, null=True)),
                ("deleted_by_cascade", models.BooleanField(default=False, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "uuid",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Uuid",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Name")),
                ("short_name", models.CharField(db_index=True, max_length=50, verbose_name="Short Name")),
                ("slug", models.SlugField(unique=True, verbose_name="Slug")),
                (
                    "vat_country",
                    models.CharField(
                        choices=[
                            ("AL", "Albania"),
                            ("AD", "Andorra"),
                            ("AT", "Austria"),
                            ("BY", "Belarus"),
                            ("BE", "Belgium"),
                            ("BA", "Bosnia and Herzegovina"),
                            ("BG", "Bulgaria"),
                            ("HR", "Croatia"),
                            ("CY", "Cyprus"),
                            ("CZ", "Czech Republic"),
                            ("DK", "Denmark"),
                            ("EE", "Estonia"),
                            ("FO", "Faroe Islands"),
                            ("FI", "Finland"),
                            ("FR", "France"),
                            ("DE", "Germany"),
                            ("GI", "Gibraltar"),
                            ("GR", "Greece"),
                            ("HU", "Hungary"),
                            ("IS", "Iceland"),
                            ("IE", "Ireland"),
                            ("IM", "Isle of Man"),
                            ("IT", "Italy"),
                            ("XK", "Kosovo"),
                            ("LV", "Latvia"),
                            ("LI", "Liechtenstein"),
                            ("LT", "Lithuania"),
                            ("LU", "Luxembourg"),
                            ("MT", "Malta"),
                            ("MD", "Moldova"),
                            ("MC", "Monaco"),
                            ("ME", "Montenegro"),
                            ("NL", "Netherlands"),
                            ("MK", "North Macedonia"),
                            ("NO", "Norway"),
                            ("PL", "Poland"),
                            ("PT", "Portugal"),
                            ("RO", "Romania"),
                            ("RU", "Russia"),
                            ("SM", "San Marino"),
                            ("RS", "Serbia"),
                            ("SK", "Slovakia"),
                            ("SI", "Slovenia"),
                            ("ES", "Spain"),
                            ("SE", "Sweden"),
                            ("CH", "Switzerland"),
                            ("UA", "Ukraine"),
                            ("GB", "United Kingdom"),
                            ("VA", "Vatican City"),
                        ],
                        default="PT",
                        max_length=50,
                        verbose_name="Vat Country",
                    ),
                ),
                ("vat_number", models.CharField(max_length=50, verbose_name="Vat Number")),
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
                (
                    "country",
                    models.CharField(
                        choices=[
                            ("AL", "Albania"),
                            ("AD", "Andorra"),
                            ("AT", "Austria"),
                            ("BY", "Belarus"),
                            ("BE", "Belgium"),
                            ("BA", "Bosnia and Herzegovina"),
                            ("BG", "Bulgaria"),
                            ("HR", "Croatia"),
                            ("CY", "Cyprus"),
                            ("CZ", "Czech Republic"),
                            ("DK", "Denmark"),
                            ("EE", "Estonia"),
                            ("FO", "Faroe Islands"),
                            ("FI", "Finland"),
                            ("FR", "France"),
                            ("DE", "Germany"),
                            ("GI", "Gibraltar"),
                            ("GR", "Greece"),
                            ("HU", "Hungary"),
                            ("IS", "Iceland"),
                            ("IE", "Ireland"),
                            ("IM", "Isle of Man"),
                            ("IT", "Italy"),
                            ("XK", "Kosovo"),
                            ("LV", "Latvia"),
                            ("LI", "Liechtenstein"),
                            ("LT", "Lithuania"),
                            ("LU", "Luxembourg"),
                            ("MT", "Malta"),
                            ("MD", "Moldova"),
                            ("MC", "Monaco"),
                            ("ME", "Montenegro"),
                            ("NL", "Netherlands"),
                            ("MK", "North Macedonia"),
                            ("NO", "Norway"),
                            ("PL", "Poland"),
                            ("PT", "Portugal"),
                            ("RO", "Romania"),
                            ("RU", "Russia"),
                            ("SM", "San Marino"),
                            ("RS", "Serbia"),
                            ("SK", "Slovakia"),
                            ("SI", "Slovenia"),
                            ("ES", "Spain"),
                            ("SE", "Sweden"),
                            ("CH", "Switzerland"),
                            ("UA", "Ukraine"),
                            ("GB", "United Kingdom"),
                            ("VA", "Vatican City"),
                        ],
                        default="PT",
                        max_length=50,
                        verbose_name="Country",
                    ),
                ),
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