# Generated by Django 3.2 on 2021-08-23 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0027_remove_order_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phi',
            field=models.CharField(default='', max_length=100),
        ),
    ]