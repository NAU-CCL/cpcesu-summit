# Generated by Django 3.2.8 on 2021-11-16 00:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('summit_auth', '0012_alter_organization_type'),
        ('summit_projects', '0010_merge_0009_auto_20210920_2056_0009_auto_20211011_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='cesu_unit',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cesu_unit', to='summit_auth.cesu', verbose_name='CESUnit'),
        ),
        migrations.AlterField(
            model_name='project',
            name='federal_agency',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='federal_agency', to='summit_auth.organization', verbose_name='Agency'),
        ),
        migrations.AlterField(
            model_name='project',
            name='partner',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='partner', to='summit_auth.organization'),
        ),
    ]
