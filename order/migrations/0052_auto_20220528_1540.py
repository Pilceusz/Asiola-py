# Generated by Django 3.2.8 on 2022-05-28 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0051_auto_20211108_1805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='paczkomat',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='paczkomat',
        ),
    ]
