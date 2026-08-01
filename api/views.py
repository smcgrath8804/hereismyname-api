from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.models import Profile
from profiles.services import (get_visible_fields, build_profile_data,)

from .serializers import ProfileSerializer

from rest_framework.permissions import IsAuthenticated


class ProfileAPIView(APIView):

    def get(self, request, username):

        profile = get_object_or_404(
            Profile,
            user__username=username,
        )

        visible_fields = get_visible_fields(
            profile,
            request.user,
        )

        serializer = ProfileSerializer(
            visible_fields
        )

        return Response(serializer.data)


class MyProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        profile = request.user.profile

        serializer = ProfileSerializer(
            build_profile_data(profile)
        )

        return Response(serializer.data)