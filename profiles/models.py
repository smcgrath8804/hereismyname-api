from django.conf import settings
from django.db import models


class Profile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    # ==== Identity ====
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
    )

    display_name = models.CharField(
        max_length=100,
        blank=True,
    )

    local_language_name = models.CharField(
        max_length=100,
        blank=True,
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    nationality = models.CharField(
        max_length=100,
        blank=True,
    )

    languages_spoken = models.CharField(
        max_length=255,
        blank=True,
    )


    # ==== Location ====
    country = models.CharField(
        max_length=100,
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )


    # ==== Contact ====
    email = models.EmailField(
        blank=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    website = models.URLField(
        blank=True,
    )


    # ==== Professional ====
    job_title = models.CharField(
        max_length=100,
        blank=True,
    )

    company = models.CharField(
        max_length=100,
        blank=True,
    )

    industry = models.CharField(
        max_length=100,
        blank=True,
    )

    skills = models.TextField(
        blank=True,
    )

    years_experience = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )


    # ==== About ====
    bio = models.TextField(
        blank=True,
    )

    interests = models.TextField(
        blank=True,
    )

    hobbies = models.TextField(
        blank=True,
    )

    def __str__(self):
        return self.display_name or self.user.username