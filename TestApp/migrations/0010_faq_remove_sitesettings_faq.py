# Generated by Django 5.1.2 on 2024-10-17 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TestApp", "0009_sitesettings"),
    ]

    operations = [
        migrations.CreateModel(
            name="FAQ",
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
                    "question",
                    models.CharField(
                        help_text="The frequently asked question", max_length=255
                    ),
                ),
                ("answer", models.TextField(help_text="The answer to the FAQ")),
            ],
        ),
        migrations.RemoveField(
            model_name="sitesettings",
            name="faq",
        ),
    ]
