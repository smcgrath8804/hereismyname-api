from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    display_name = models.CharField(max_length=100)
    local_language_name = models.CharField(max_length=100, blank=True)

    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    job_title = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)

    bio = models.TextField(blank=True)

    def __str__(self):
        return self.display_name