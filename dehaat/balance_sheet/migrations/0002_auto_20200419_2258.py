# Generated by Django 2.2.12 on 2020-04-19 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balance_sheet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balancesheet',
            name='query_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
    ]