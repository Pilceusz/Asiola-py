# Generated by Django 3.2 on 2021-08-26 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0038_auto_20210826_0900'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='size',
        ),
    ]
