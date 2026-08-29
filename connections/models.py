from django.conf import settings
from django.db import models

from .constants import RELATIONSHIP_TYPES

class Connection(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="owned_connections",
        on_delete=models.CASCADE,
    )

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="requested_connections",
        on_delete=models.CASCADE,
    )

    relationship = models.CharField(
        max_length=20,
        choices=RELATIONSHIP_TYPES,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = (
            "owner",
            "requester",
        )

    def __str__(self):
        if self.relationship:
            return f"{self.requester} to {self.owner} ({self.relationship})"
        return f"{self.requester} to {self.owner} (Pending)"