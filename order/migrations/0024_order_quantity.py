# Generated by Django 3.2 on 2021-08-23 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0023_remove_order_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.CharField(default='', max_length=200),
        ),
    ]