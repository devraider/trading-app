# Generated by Django 5.1.4 on 2024-12-14 19:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trading", "0006_alter_transaction_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]