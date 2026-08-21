from django.conf import settings
from django.db import models

from .constants import PLATFORM_CHOICES


class ProfileLink(models.Model):

    profile = models.ForeignKey(
        "profiles.Profile",
        on_delete=models.CASCADE,
        related_name="links",
    )

    platform = models.CharField(
        max_length=30,
        choices=PLATFORM_CHOICES,
    )

    platform_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Only used when Platform is 'Other'.",
    )

    label = models.CharField(
        max_length=100,
        blank=True,
    )

    url = models.URLField()

    display_order = models.PositiveSmallIntegerField(
        default=0,
    )

    class Meta:

        ordering = [
            "display_order",
            "platform",
        ]

    def __str__(self):

        if self.label:
            return self.label

        return self.get_platform_display()