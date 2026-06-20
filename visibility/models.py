from django.conf import settings
from django.db import models


class VisibilityRule(models.Model):

    FIELD_CHOICES = [
        ("email", "Email"),
        ("phone", "Phone"),
        ("job_title", "Job Title"),
        ("company", "Company"),
        ("bio", "Bio"),
    ]

    CONNECTION_TYPES = [
        ("personal", "Personal"),
        ("professional", "Professional"),
        ("general", "General"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    field_name = models.CharField(
        max_length=50,
        choices=FIELD_CHOICES
    )

    visible_to = models.CharField(
        max_length=20,
        choices=CONNECTION_TYPES
    )