from django.shortcuts import get_object_or_404, render

from .models import Profile
from connections.models import Connection
from visibility.models import VisibilityRule
from users.models import User


def profile_view(request, profile_id):

    profile = get_object_or_404(
        Profile,
        id=profile_id
    )

    viewer_username = request.GET.get("viewer")

    visible_fields = {}

    if viewer_username:

        try:

            viewer = User.objects.get(
                username=viewer_username
            )

            connection = Connection.objects.get(
                from_user=viewer,
                to_user=profile.user
            )

            rules = VisibilityRule.objects.filter(
                owner=profile.user,
                visible_to=connection.connection_type
            )

            for rule in rules:

                visible_fields[rule.field_name] = getattr(
                    profile,
                    rule.field_name
                )

        except (
            User.DoesNotExist,
            Connection.DoesNotExist
        ):
            pass

    return render(
        request,
        "profiles/profile.html",
        {
            "profile": profile,
            "visible_fields": visible_fields
        }
    )