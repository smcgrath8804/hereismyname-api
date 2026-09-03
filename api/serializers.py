from rest_framework import serializers

from visibility.constants import PROFILE_FIELDS

from links.constants import PLATFORM_CHOICES

from connections.constants import RELATIONSHIP_TYPES


## View the profile
class ProfileSerializer(serializers.Serializer):
    ## ==== Identity ====
    profile_picture = serializers.ImageField(required=False)
    display_name = serializers.CharField(required=False)
    display_name_2 = serializers.CharField(required=False)
    display_name_3 = serializers.CharField(required=False)
    local_language_name = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    nationality = serializers.CharField(required=False)
    languages_spoken = serializers.CharField(required=False)

    ## ==== Location ====
    country = serializers.CharField(required=False)
    city = serializers.CharField(required=False)

    ## ==== Contact ====
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)
    website = serializers.URLField(required=False)

    ## ==== Professional ====
    job_title = serializers.CharField(required=False)
    company = serializers.CharField(required=False)
    industry = serializers.CharField(required=False)
    skills = serializers.CharField(required=False)
    years_experience = serializers.IntegerField(required=False)

    ## ==== About ====
    bio = serializers.CharField(required=False)
    interests = serializers.CharField(required=False)
    hobbies = serializers.CharField(required=False)


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True) ## Password will never be displayed in API


 ## Add the ability to update individual fields in the profile
class UpdateProfileSerializer(serializers.Serializer):

    ## ==== Identity ====
    profile_picture = serializers.ImageField(required=False)
    display_name = serializers.CharField(required=False)
    display_name_2 = serializers.CharField(required=False)
    display_name_3 = serializers.CharField(required=False)
    local_language_name = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    nationality = serializers.CharField(required=False)
    languages_spoken = serializers.CharField(required=False)

    ## ==== Location ====
    country = serializers.CharField(required=False)
    city = serializers.CharField(required=False)

    ## ==== Contact ====
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)
    website = serializers.URLField(required=False)

    ## ==== Professional ====
    job_title = serializers.CharField(required=False)
    company = serializers.CharField(required=False)
    industry = serializers.CharField(required=False)
    skills = serializers.CharField(required=False)
    years_experience = serializers.IntegerField(required=False)

    ## ==== About ====
    bio = serializers.CharField(required=False)
    interests = serializers.CharField(required=False)
    hobbies = serializers.CharField(required=False)

# #conection owned by the authenticated user.
class ConnectionSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    username = serializers.CharField()
    display_name = serializers.CharField()
    relationship = serializers.CharField()

## allow owner to change the relationship type
class UpdateConnectionSerializer(serializers.Serializer):

    relationship = serializers.ChoiceField(
        choices = RELATIONSHIP_TYPES,
    )

## connection requests awaiting review
class PendingConnectionSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    username = serializers.CharField()
    display_name = serializers.CharField()

## Send connection request to another user
class ConnectionRequestSerializer(serializers.Serializer):

    username = serializers.CharField()


## Review a pending connection request
class ReviewConnectionSerializer(serializers.Serializer):

    relationship = serializers.ChoiceField(
        choices = RELATIONSHIP_TYPES,
    )


## Profile field visibility rule used by the API.
class VisibilityFieldRuleSerializer(serializers.Serializer):

    field_name = serializers.ChoiceField(
        choices=[
            field_name
            for field_name, _ in PROFILE_FIELDS
        ]
    )

    visible_to = serializers.ListField(
        child=serializers.ChoiceField(
            choices=RELATIONSHIP_TYPES,
        ),
        required=False,
        allow_empty=True,
    )


#' Profile link visibility rule used by API
class VisibilityLinkRuleSerializer(serializers.Serializer):

    link_id = serializers.IntegerField()

    visible_to = serializers.ListField(
        child=serializers.ChoiceField(
            choices=RELATIONSHIP_TYPES,
        ),
        required=False,
        allow_empty=True,
    )


## Combined visibility
class VisibilityRulesSerializer(serializers.Serializer):

    profile_fields = VisibilityFieldRuleSerializer(
        many=True,
        required=False,
    )

    profile_links = VisibilityLinkRuleSerializer(
        many=True,
        required=False,
    )

## Profile link shown through the API.
class ProfileLinkSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    platform = serializers.CharField()
    platform_name = serializers.CharField()
    label = serializers.CharField()
    url = serializers.URLField()
    display_order = serializers.IntegerField()


## Create a profile link through the API - taken from ProfileLinkForm.
class CreateProfileLinkSerializer(serializers.Serializer):

    platform = serializers.ChoiceField(
        choices=PLATFORM_CHOICES,
    )

    platform_name = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    label = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    url = serializers.URLField()

    display_order = serializers.IntegerField(
        required=False,
    )

    def validate(self, data):

        platform = data.get("platform")
        platform_name = data.get("platform_name")

        ## When other selected, input customer value
        if platform == "other" and not platform_name:

            raise serializers.ValidationError({
                "platform_name": "Please enter a platform name.",
            })

        ## clearing platform_name for normal platforms.
        elif platform != "other":

            data["platform_name"] = ""

        return data


## Update a profile link through the API. Partial updates, all fields optional
class UpdateProfileLinkSerializer(serializers.Serializer):

    platform = serializers.ChoiceField(
        choices=PLATFORM_CHOICES,
        required=False,
    )

    platform_name = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    label = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    url = serializers.URLField(
        required=False,
    )

    display_order = serializers.IntegerField(
        required=False,
    )

    def validate(self, data):

        platform = data.get("platform")
        platform_name = data.get("platform_name")

        ## When other selected, input customer value
        if platform == "other" and not platform_name:

            raise serializers.ValidationError({
                "platform_name": "Please enter a platform name.",
            })

        ## clear platform_name for normal platforms
        elif platform and platform != "other":

            data["platform_name"] = ""

        return data