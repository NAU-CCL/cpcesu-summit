# Generated by Django 3.2.8 on 2022-08-23 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summit_projects', '0020_auto_20220614_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modification',
            name='mod_status',
            field=models.CharField(blank=True, choices=[('POTENTIAL', 'Potential'), ('PENDING', 'Pending'), ('APPROVED', 'Approvived'), ('AWARDED', 'Awarded'), ('CLOSED', 'Closed')], default=('POTENTIAL', 'Potential'), max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='fiscal_year',
            field=models.PositiveSmallIntegerField(blank=True, default=2022, null=True, verbose_name='Fiscal Year'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(blank=True, choices=[('DRAFT', 'Drafting'), ('APPROVED', 'Approved'), ('EXECUTED', 'Executed'), ('CLOSED', 'Closed')], default=('DRAFT', 'Drafting'), max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='type',
            field=models.CharField(blank=True, choices=[('NONE', 'None'), ('EDUCATION', 'Education'), ('RESEARCH', 'Research'), ('TECHNICAL', 'Technical Assistance')], help_text='Type of project implemented', max_length=50, verbose_name='Project Type'),
        ),
    ]
