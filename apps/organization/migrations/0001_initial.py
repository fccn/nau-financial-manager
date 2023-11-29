# Generated by Django 4.2.5 on 2023-11-29 09:36

from django.db import migrations, models


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
                ("email", models.CharField(max_length=255, null=True, verbose_name="Email")),
            ],
            options={
                "verbose_name": "Organization",
                "verbose_name_plural": "Organizations",
            },
        ),
    ]
