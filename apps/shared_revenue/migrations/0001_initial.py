import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import apps.billing.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("organization", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PartnershipLevel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(db_index=True, editable=False, null=True)),
                ("deleted_by_cascade", models.BooleanField(default=False, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="Name")),
                ("description", models.CharField(blank=True, max_length=255, null=True, verbose_name="Description")),
                (
                    "percentage",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=3,
                        unique=True,
                        validators=[
                            django.core.validators.MaxValueValidator(1),
                            django.core.validators.MinValueValidator(0),
                        ],
                        verbose_name="Value",
                    ),
                ),
            ],
            options={
                "verbose_name": "Partnership level",
                "verbose_name_plural": "Partnership levels",
            },
        ),
        migrations.CreateModel(
            name="ShareExecution",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(db_index=True, editable=False, null=True)),
                ("deleted_by_cascade", models.BooleanField(default=False, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("revenue_configuration", models.JSONField(verbose_name="Revenue Configuration")),
                ("percentage", models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Percentage")),
                ("value", models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Value")),
                ("receipt", models.CharField(max_length=50, verbose_name=apps.billing.models.Receipt)),
                ("executed", models.BooleanField(default=False, verbose_name="Executed")),
                ("response_payload", models.JSONField(verbose_name="Response Payload")),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="share_organizations",
                        to="organization.organization",
                    ),
                ),
            ],
            options={
                "verbose_name": "Share exectution",
                "verbose_name_plural": "Share exectutions",
            },
        ),
        migrations.CreateModel(
            name="RevenueConfiguration",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(db_index=True, editable=False, null=True)),
                ("deleted_by_cascade", models.BooleanField(default=False, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("course_code", models.CharField(blank=True, max_length=50, null=True, verbose_name="Course code")),
                ("start_date", models.DateTimeField(auto_now_add=True, verbose_name="Start date")),
                ("end_date", models.DateTimeField(blank=True, null=True, verbose_name="End date")),
                (
                    "organization",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="revenue_organizations",
                        to="organization.organization",
                    ),
                ),
                (
                    "partnership_level",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="revenue_partnership_levels",
                        to="shared_revenue.partnershiplevel",
                    ),
                ),
            ],
            options={
                "verbose_name": "Revenue configuration",
                "verbose_name_plural": "Revenue configurations",
            },
        ),
        migrations.AddConstraint(
            model_name="revenueconfiguration",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(("course_code__isnull", True), ("organization__isnull", True), _negated=True),
                    models.Q(("course_code__exact", ""), ("organization__exact", ""), _negated=True),
                    models.Q(
                        models.Q(("course_code__isnull", True), ("organization__isnull", False)),
                        models.Q(("course_code__isnull", False), ("organization__isnull", True)),
                        _connector="OR",
                    ),
                ),
                name="organization_and_course_code_not_null",
            ),
        ),
    ]
