# Generated by Django 5.2 on 2025-04-13 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads_app', '0003_carad_created_updated_addition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carad',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='carad',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
