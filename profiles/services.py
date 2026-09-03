from connections.models import Connection
from visibility.models import VisibilityRule

## Build a reusable profile data dictionary
def build_profile_data(profile):

    return {
        # ==== Identity ====
        "profile_picture": profile.profile_picture,
        "display_name": profile.display_name,
        "display_name_2": profile.display_name_2,
        "display_name_3": profile.display_name_3,
        "local_language_name": profile.local_language_name,
        "date_of_birth": profile.date_of_birth,
        "nationality": profile.nationality,
        "languages_spoken": profile.languages_spoken,

        # ==== Location ====
        "country": profile.country,
        "city": profile.city,

        # ==== Contact ====
        "email": profile.email,
        "phone": profile.phone,
        "website": profile.website,

        # ==== Professional ====
        "job_title": profile.job_title,
        "company": profile.company,
        "industry": profile.industry,
        "skills": profile.skills,
        "years_experience": profile.years_experience,

        # ==== About ====
        "bio": profile.bio,
        "interests": profile.interests,
        "hobbies": profile.hobbies,
    }

def get_relationship(viewer, owner):

    if viewer.is_authenticated:

        if viewer == owner:
            return "owner"

        try:

            connection = Connection.objects.get(
                owner = owner,
                requester = viewer,
            )

            if connection.relationship is None:
                return "public"

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
        return build_profile_data(profile)

    visible_fields = {}

    ## Show public fields plus fields for the viewer's relationship type
    rules = VisibilityRule.objects.filter(
        owner = profile.user,
        visible_to__in=["public", relationship]
    )

    for rule in rules:

        visible_fields[rule.field_name] = getattr(
            profile,
            rule.field_name
        )

    return visible_fields

def get_visible_display_name(visible_fields, user):
    ## Choose the first visible display name for lists and search results
    for field_name in [
        "display_name",
        "display_name_2",
        "display_name_3",
        "local_language_name",
    ]:
        if visible_fields.get(field_name):
            return visible_fields[field_name]

    return user.username


def build_visible_profile_summary(user, viewer):
    ## Build safe profile details for search and connection lists
    visible_fields = get_visible_fields(
        user.profile,
        viewer,
    )

    return {
        "user": user,
        "display_name": get_visible_display_name(
            visible_fields,
            user,
        ),
        "profile_picture": visible_fields.get("profile_picture"),
    }