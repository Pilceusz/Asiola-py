# Generated by Django 3.2 on 2021-08-26 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0034_alter_order_quant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='quant',
            field=models.DecimalField(decimal_places=2, default='', max_digits=10),
        ),
    ]
