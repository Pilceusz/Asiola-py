# Generated by Django 3.2 on 2021-07-27 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_remove_product_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')], default='draft', max_length=10),
        ),
    ]
