from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import (IsAuthenticated, AllowAny)

from profiles.models import Profile
from profiles.services import (get_visible_fields, build_profile_data,)

from .serializers import (LoginSerializer, ProfileSerializer, UpdateProfileSerializer, ConnectionSerializer, UpdateConnectionSerializer,)

from django.contrib.auth import authenticate
from rest_framework import status

from connections.models import Connection

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

    def patch(self, request):

        profile = request.user.profile

        serializer = UpdateProfileSerializer(
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True
        )

        for field, value in serializer.validated_data.items():

            setattr(profile, field, value,)

        profile.save()

        return Response(
            ProfileSerializer(build_profile_data(profile)).data
        )

# Return all connections for the logged-in user.
class ConnectionsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        connections = Connection.objects.filter(
            owner=request.user
        ).exclude(
            relationship__isnull=True
        )

        data = []

        for connection in connections:

            data.append({
                "id": connection.id,
                "username": connection.requester.username,
                "display_name": connection.requester.profile.display_name,
                "relationship": connection.relationship,
            })

        serializer = ConnectionSerializer(
            data,
            many=True,
        )

        return Response(serializer.data)

# Allow the owner to update one of their connections
class ConnectionDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, connection_id):

        connection = get_object_or_404(
            Connection,
            id=connection_id,
            owner=request.user, # Only return connectons for logged in user
        )

        serializer = UpdateConnectionSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        connection.relationship = serializer.validated_data["relationship"]

        connection.save()

        return Response(
            ConnectionSerializer(
                {
                    "id": connection.id,
                    "username": connection.requester.username,
                    "display_name": connection.requester.profile.display_name,
                    "relationship": connection.relationship,
                }
            ).data
        )

class LoginAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if user is None:

            return Response(
                {
                    "error": "Invalid username or password."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token, created = Token.objects.get_or_create(
            user=user
        )

        return Response(
            {
                "token": token.key
            }
        )