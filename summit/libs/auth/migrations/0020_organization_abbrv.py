# Generated by Django 3.2.8 on 2022-04-20 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summit_auth', '0019_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='abbrv',
            field=models.TextField(blank=True, max_length=300),
        ),
    ]
