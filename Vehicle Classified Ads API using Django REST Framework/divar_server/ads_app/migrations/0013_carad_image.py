# Generated by Django 5.2 on 2025-04-14 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads_app', '0012_review_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='carad',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='car_images/'),
        ),
    ]
