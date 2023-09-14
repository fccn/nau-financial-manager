import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("organization", "0001_initial"),
        ("billing", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="receipt",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="organization_receipts",
                to="organization.organization",
            ),
        ),
    ]
