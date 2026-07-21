from django.conf import settings
from django.db import models
from .constants import PROFILE_FIELDS


class VisibilityRule(models.Model):

    FIELD_CHOICES = PROFILE_FIELDS

    CONNECTION_TYPES = [
        ("public", "Public"),
        ("professional", "Professional"),
        ("personal", "Personal"),
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "field_name", "visible_to"],
                name="unique_visibility_rule",
            )
        ]