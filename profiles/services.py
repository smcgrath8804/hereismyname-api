from connections.models import Connection
from visibility.models import VisibilityRule


def get_relationship(viewer, owner):

    if viewer.is_authenticated:

        if viewer == owner:
            return "owner"

        try:

            connection = Connection.objects.get(
                owner=owner,
                requester=viewer,
            )

            return connection.relationship

        except Connection.DoesNotExist:
            pass

    return "public"


def get_visible_fields(profile, viewer):

    relationship = get_relationship(
        viewer,
        profile.user
    )

    if relationship == "owner":

        return {
            "display_name": profile.display_name,
            "local_language_name": profile.local_language_name,
            "email": profile.email,
            "phone": profile.phone,
            "job_title": profile.job_title,
            "company": profile.company,
            "bio": profile.bio,
        }

    visible_fields = {}

    rules = VisibilityRule.objects.filter(
        owner=profile.user,
        visible_to=relationship
    )

    for rule in rules:

        visible_fields[rule.field_name] = getattr(
            profile,
            rule.field_name
        )

    return visible_fields