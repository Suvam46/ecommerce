# Generated by Django 5.1.2 on 2024-10-16 08:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TestApp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="ad",
            name="favorites",
            field=models.ManyToManyField(
                blank=True, related_name="favorite_ads", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
