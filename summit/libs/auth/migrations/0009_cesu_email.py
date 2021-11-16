# Generated by Django 3.2.8 on 2021-11-02 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summit_auth', '0008_alter_organization_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='cesu',
            name='email',
            field=models.EmailField(default='default@default.email', max_length=255, verbose_name='Contact Email Address'),
            preserve_default=False,
        ),
    ]
