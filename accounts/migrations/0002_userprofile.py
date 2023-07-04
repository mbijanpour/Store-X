# Generated by Django 4.2.2 on 2023-07-04 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="userProfile",
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
                    "profile_picture",
                    models.ImageField(
                        blank=True, null=True, upload_to="users/profile_pictures"
                    ),
                ),
                (
                    "cover_photo",
                    models.ImageField(
                        blank=True, null=True, upload_to="users/cover_photos"
                    ),
                ),
                ("first_address", models.TextField(blank=True, null=True)),
                ("second_address", models.TextField(blank=True, null=True)),
                ("province", models.CharField(blank=True, max_length=50, null=True)),
                ("pin_code", models.CharField(blank=True, max_length=6, null=True)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("modified_date", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]