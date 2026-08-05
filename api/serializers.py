from rest_framework import serializers

## View the profile
class ProfileSerializer(serializers.Serializer):

    display_name = serializers.CharField(required=False)
    local_language_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)
    job_title = serializers.CharField(required=False)
    company = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True) ## Password will never be displayed in API

 ## Add the ability to update individual fields in the profile
class UpdateProfileSerializer(serializers.Serializer):

    display_name = serializers.CharField(required=False)
    local_language_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)
    job_title = serializers.CharField(required=False)
    company = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)

# conection owned by the authenticated user.
class ConnectionSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    username = serializers.CharField()
    display_name = serializers.CharField()
    relationship = serializers.CharField()

# Allow owner to change the relationship type
class UpdateConnectionSerializer(serializers.Serializer):

    relationship = serializers.ChoiceField(
        choices = ["public", "personal", "professional", "general",]
    )

# connection requests awaiting review
class PendingConnectionSerializer(serializers.Serializer):


    id = serializers.IntegerField()
    username = serializers.CharField()
    display_name = serializers.CharField()

# Send a connection request to another user
class ConnectionRequestSerializer(serializers.Serializer):

    username = serializers.CharField()


# Review a pending connection request
class ReviewConnectionSerializer(serializers.Serializer):

    relationship = serializers.ChoiceField(
        choices=[
            "public",
            "personal",
            "professional",
            "general",
        ]
    )