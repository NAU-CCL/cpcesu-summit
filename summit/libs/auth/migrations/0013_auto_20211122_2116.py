# Generated by Django 3.2.8 on 2021-11-23 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summit_auth', '0012_alter_organization_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='email',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='user',
        ),
        migrations.AddField(
            model_name='organization',
            name='contact',
            field=models.TextField(blank=True, max_length=300),
        ),
    ]
