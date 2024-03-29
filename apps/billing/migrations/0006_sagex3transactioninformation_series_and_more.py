# Generated by Django 4.2.8 on 2024-03-14 11:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("billing", "0005_alter_transaction_vat_identification_country"),
    ]

    operations = [
        migrations.AddField(
            model_name="sagex3transactioninformation",
            name="series",
            field=models.CharField(
                default="FRN",
                help_text="The transaction series, by default we should use FRN, to fix date issues use FRX",
                max_length=50,
                verbose_name="Serie",
            ),
        ),
    ]
