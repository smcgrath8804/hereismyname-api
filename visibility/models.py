from django.conf import settings
from django.db import models
from .constants import PROFILE_FIELDS

from connections.constants import RELATIONSHIP_TYPES


class VisibilityRule(models.Model):

    FIELD_CHOICES = PROFILE_FIELDS

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
        choices=RELATIONSHIP_TYPES
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "field_name", "visible_to"],
                name="unique_visibility_rule",
            )
        ]

    def __str__(self):
        return f"{self.field_name} - {self.visible_to}"


class LinkVisibilityRule(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    link = models.ForeignKey(
        "links.ProfileLink",
        on_delete=models.CASCADE,
        related_name="visibility_rules",
    )

    visible_to = models.CharField(
        max_length=20,
        choices=RELATIONSHIP_TYPES,
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "owner",
                    "link",
                    "visible_to",
                ],
                name="unique_link_visibility_rule",
            )
        ]

    def __str__(self):

        return (
            f"{self.link} - {self.visible_to}"
        )