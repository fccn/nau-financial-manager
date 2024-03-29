# Generated by Django 4.2.8 on 2024-03-06 16:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("billing", "0002_transactionitem_discount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sagex3transactioninformation",
            name="status",
            field=models.CharField(
                choices=[("pending", "pending"), ("success", "success"), ("failed", "failed")],
                default="pending",
                max_length=255,
            ),
        ),
    ]
