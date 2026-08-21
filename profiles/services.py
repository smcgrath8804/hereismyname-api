from connections.models import Connection
from visibility.models import VisibilityRule

## Reusable way to build my profiles each time
def build_profile_data(profile):

    return {

        # ==== Identity ====
        "profile_picture": profile.profile_picture,
        "display_name": profile.display_name,
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
                owner=owner,
                requester=viewer,
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

    # print("Relationship:", relationship)
    if relationship == "owner":
        return build_profile_data(profile)

    visible_fields = {}

    rules = VisibilityRule.objects.filter(
        owner=profile.user,
        visible_to=relationship
    )

    # print("Rules:", list(rules.values_list("field_name", flat=True)))

    for rule in rules:

        visible_fields[rule.field_name] = getattr(
            profile,
            rule.field_name
        )

    return visible_fields