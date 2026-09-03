from django.utils import timezone

from profiles.services import build_visible_profile_summary

from .constants import RELATIONSHIP_TYPES

from .models import Connection


def build_connection_data(connection, viewer):
    ## Build a consistent API representation of a connection for re-use
    profile_summary = build_visible_profile_summary(
        connection.requester,
        viewer,
    )

    return {
        "id": connection.id,
        "username": connection.requester.username,
        "display_name": profile_summary["display_name"],
        "relationship": connection.relationship,
    }

def build_pending_connection_data(connection, viewer):
    ## Build a consistent API representation of a pending connection request
    profile_summary = build_visible_profile_summary(
        connection.requester,
        viewer,
    )

    return {
        "id": connection.id,
        "username": connection.requester.username,
        "display_name": profile_summary["display_name"],
    }

def create_connection_request(owner, requester):
    ## Create a connection request if one does not already exist
    if owner == requester:
        raise ValueError(
            "You can't send a connection request to yourself."
        )

    connection, created = Connection.objects.get_or_create(
        owner=owner,
        requester=requester,
    )
    return connection, created


def review_connection_request(connection, relationship):
    ## Review a pending connection request
    valid_relationships = {
        choice[0]
        for choice in RELATIONSHIP_TYPES
    }

    if relationship not in valid_relationships:
        raise ValueError(
            "Invalid relationship selected."
        )

    connection.relationship = relationship
    connection.reviewed_at = timezone.now()
    connection.save()

    return connection