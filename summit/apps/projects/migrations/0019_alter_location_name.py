# Generated by Django 3.2.8 on 2022-04-25 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summit_projects', '0018_auto_20220425_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.TextField(max_length=255),
        ),
    ]
