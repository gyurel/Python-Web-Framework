# Generated by Django 4.0.3 on 2022-04-02 17:06

import common.validators
import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_alter_profile_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='age',
        ),
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=50, null=True, validators=[django.core.validators.MinLengthValidator(5)]),
        ),
        migrations.AddField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(null=True, validators=[common.validators.MaxDateValidator(datetime.date(2022, 4, 2)), common.validators.MinDateValidator(120)]),
        ),
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('Not specified', 'Not specified'), ('Man', 'Man'), ('Woman', 'Woman'), ("Don't want to specify", "Don't want to specify")], default='Not specified', max_length=21),
        ),
        migrations.AddField(
            model_name='profile',
            name='post_code',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True, validators=[django.core.validators.MinValueValidator(1000, message='Post code should be greater than 999'), django.core.validators.MaxValueValidator(9999, message='Value should not exceed 9999')]),
        ),
        migrations.AddField(
            model_name='profile',
            name='town',
            field=models.CharField(blank=True, max_length=25, null=True, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
    ]
