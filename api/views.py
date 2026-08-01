from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.models import Profile
from profiles.services import get_visible_fields

from .serializers import VisibleProfileSerializer


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

        serializer = VisibleProfileSerializer(
            visible_fields
        )

        return Response(serializer.data)