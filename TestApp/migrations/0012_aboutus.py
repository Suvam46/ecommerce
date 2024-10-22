# Generated by Django 5.1.2 on 2024-10-17 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TestApp", "0011_teammember"),
    ]

    operations = [
        migrations.CreateModel(
            name="AboutUs",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "introduction",
                    models.TextField(
                        help_text="Introduction text for the 'About Us' section"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        help_text="Image for the 'About Us' section", upload_to="about/"
                    ),
                ),
            ],
        ),
    ]
