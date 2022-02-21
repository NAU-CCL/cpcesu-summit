# Generated by Django 3.2.8 on 2022-02-20 21:19

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summit_projects', '0014_alter_project_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='added_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Initial funding amount (USD)', max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('9999999.99'))], verbose_name='Initial'),
        ),
        migrations.AddField(
            model_name='project',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Initial funding amount (USD)', max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('9999999.99'))], verbose_name='Initial'),
        ),
    ]
