# Generated by Django 5.2 on 2025-05-03 14:24

import ads_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads_app', '0020_alter_carad_ad_user_alter_motorcyclead_ad_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(validators=[ads_app.models.no_offensive_words]),
        ),
    ]
