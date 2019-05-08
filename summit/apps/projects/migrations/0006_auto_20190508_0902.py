# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-08 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summit_projects', '0005_auto_20190507_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(blank=True, choices=[('DRAFT', 'Drafting'), ('APPROVED', 'Approved'), ('EXECUTED', 'Executed'), ('CLOSED', 'Closed')], default=('DRAFT', 'Drafting'), max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='youth_vets',
            field=models.CharField(choices=[('NO', 'NO'), ('YES', 'YES')], default=('NO', 'NO'), max_length=500, verbose_name='Youth/Vets'),
        ),
    ]
