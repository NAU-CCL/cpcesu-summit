# Generated by Django 3.2.4 on 2021-09-02 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summit_projects', '0006_modification_mod_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
