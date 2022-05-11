# Generated by Django 3.2.8 on 2022-02-20 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('summit_auth', '0014_userprofile_cesu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='assigned_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='summit_auth.organization', verbose_name='Assigned Organization'),
        ),
    ]