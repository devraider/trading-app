# Generated by Django 5.1.4 on 2024-12-14 19:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trading", "0004_transaction_trading_tra_symbol_e8b80a_idx_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 12, 14, 19, 51, 13, 86321, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
