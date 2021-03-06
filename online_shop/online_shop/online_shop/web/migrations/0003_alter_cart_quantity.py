# Generated by Django 4.0.3 on 2022-04-08 18:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_rename_product_id_favorites_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=1, validators=[django.core.validators.MinValueValidator(0, message='The quantity can not be less than zero!')]),
        ),
    ]
