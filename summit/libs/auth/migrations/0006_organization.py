# Generated by Django 3.2.8 on 2021-10-12 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summit_auth', '0005_auto_20210815_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('description', models.TextField(blank=True, max_length=300)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
