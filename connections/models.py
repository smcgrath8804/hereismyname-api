from django.conf import settings
from django.db import models


class Connection(models.Model):

    CONNECTION_TYPES = [
        ("personal", "Personal"),
        ("professional", "Professional"),
        ("general", "General"),
    ]

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="sent_connections",
        on_delete=models.CASCADE
    )

    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_connections",
        on_delete=models.CASCADE
    )

    connection_type = models.CharField(
        max_length=20,
        choices=CONNECTION_TYPES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "from_user",
            "to_user"
        )