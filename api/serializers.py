from rest_framework import serializers


class VisibleProfileSerializer(serializers.Serializer):

    display_name = serializers.CharField(required=False)
    local_language_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)
    job_title = serializers.CharField(required=False)
    company = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)