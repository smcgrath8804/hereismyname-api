from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import (IsAuthenticated, AllowAny)

from profiles.models import Profile
from profiles.services import (get_visible_fields, build_profile_data,)


from .serializers import (LoginSerializer, ProfileSerializer, UpdateProfileSerializer, ConnectionSerializer,
    UpdateConnectionSerializer, PendingConnectionSerializer, ConnectionRequestSerializer, ReviewConnectionSerializer,
    VisibilityRulesSerializer,
)

from django.contrib.auth import (authenticate, get_user_model)
from rest_framework import status

from connections.models import Connection
from connections.services import (build_connection_data, build_pending_connection_data, create_connection_request,
                                  review_connection_request,)
from visibility.models import VisibilityRule, LinkVisibilityRule
from visibility.constants import PROFILE_FIELDS
from links.models import ProfileLink


from drf_spectacular.utils import extend_schema

User = get_user_model()

class LoginAPIView(APIView):

    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={200: None},
    )
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

        data = [
            build_connection_data(connection)
            for connection in connections
        ]

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
                build_connection_data(connection)
            ).data
        )

# Return pending connection requests for authenticated user
class PendingConnectionsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        pending = Connection.objects.filter(
            owner=request.user,
            relationship__isnull=True,
        )

        data = [
            build_pending_connection_data(connection)
            for connection in pending
        ]

        serializer = PendingConnectionSerializer(
            data,
            many=True,
        )

        return Response(serializer.data)

# Allow the authenticated user to send a connection request
class ConnectionRequestAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ConnectionRequestSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        owner = get_object_or_404(
            User,
            username=serializer.validated_data["username"],
        )

        try:

            connection, created = create_connection_request(
                owner,
                request.user,
            )

        except ValueError as error:

            return Response(
                {
                    "error": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if created:

            return Response(
                {
                    "message": "Connection request sent."
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "error": "Connection request already exists."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# Review a pending connection request
class ReviewConnectionAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, connection_id):

        connection = get_object_or_404(
            Connection,
            id=connection_id,
            owner=request.user,
            relationship__isnull=True,
        )

        serializer = ReviewConnectionSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            review_connection_request(
                connection,
                serializer.validated_data["relationship"],
            )

        except ValueError as error:

            return Response(
                {
                    "error": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            ConnectionSerializer(
                build_connection_data(connection)
            ).data
        )

## Manage visibility rules belonging to the authenticated user.
class VisibilityRulesAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        ## Return both profile field and profile link visibilitys

        field_rules = VisibilityRule.objects.filter(
            owner=request.user,
        )

        link_rules = LinkVisibilityRule.objects.filter(
            owner=request.user,
        )

        field_visibility = []

        for field_name, _ in PROFILE_FIELDS:

            visible_to = [
                rule.visible_to
                for rule in field_rules
                if rule.field_name == field_name
            ]

            field_visibility.append({
                "field_name": field_name,
                "visible_to": visible_to,
            })

        link_visibility = []

        for link in ProfileLink.objects.filter(
            profile=request.user.profile,
        ):

            visible_to = [
                rule.visible_to
                for rule in link_rules
                if rule.link_id == link.id
            ]

            link_visibility.append({
                "link_id": link.id,
                "visible_to": visible_to,
            })

        serializer = VisibilityRulesSerializer({
            "profile_fields": field_visibility,
            "profile_links": link_visibility,
        })

        return Response(serializer.data)

    def patch(self, request):
        # Update profile field and/or profile link visibility rules.

        serializer = VisibilityRulesSerializer(
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        data = serializer.validated_data

        if "profile_fields" in data:

            VisibilityRule.objects.filter(
                owner=request.user,
            ).delete()

            for field in data["profile_fields"]:

                field_name = field["field_name"]

                for relationship in set(
                    field.get("visible_to", [])
                ):

                    VisibilityRule.objects.create(
                        owner=request.user,
                        field_name=field_name,
                        visible_to=relationship,
                    )

        if "profile_links" in data:

            LinkVisibilityRule.objects.filter(
                owner=request.user,
            ).delete()

            for link_data in data["profile_links"]:

                link = get_object_or_404(
                    ProfileLink,
                    id=link_data["link_id"],
                    profile=request.user.profile,
                )

                for relationship in set(
                    link_data.get("visible_to", [])
                ):

                    LinkVisibilityRule.objects.create(
                        owner=request.user,
                        link=link,
                        visible_to=relationship,
                    )

        return self.get(request)