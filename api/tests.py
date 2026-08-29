from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from links.models import ProfileLink
from visibility.models import VisibilityRule, LinkVisibilityRule

User = get_user_model()


class APILinkAndVisibilityTests(APITestCase):
    """
    ## References:
    ## Django testing tools: https://docs.djangoproject.com/en/6.0/topics/testing/tools/

    ## Django REST Framework API testing: https://www.django-rest-framework.org/api-guide/testing/
    """

    def setUp(self):
        ## Create two users,first user owns the test data, second owns separate data
        self.owner = User.objects.create_user(
            username="apiowner",
            email="apiowner@example.com",
            password="Test123!",
        )

        self.other_user = User.objects.create_user(
            username="apiother",
            email="apiother@example.com",
            password="Test123!",
        )

        ## Ceate tokens manually so tests can authenticate
        self.owner_token = Token.objects.create(
            user=self.owner,
        )

        self.other_token = Token.objects.create(
            user=self.other_user,
        )

        ## This link belongs to the main test user

        self.owner_link = ProfileLink.objects.create(
            profile=self.owner.profile,
            platform="github",
            label="API Owner GitHub",
            url="https://github.com/apiowner",
            display_order=0,
        )

        ## Link belongs to another user, ensure the API blocks edits and deletes on data the logged-in user doesn't own
        self.other_link = ProfileLink.objects.create(
            profile=self.other_user.profile,
            platform="linkedin",
            label="API Other LinkedIn",
            url="https://linkedin.com/in/apiother",
            display_order=0,
        )

    def authenticate_as_owner(self):
        ## use this to avoid repeating the token header in every test.
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.owner_token.key}"
        )

    def test_login_returns_token(self):
        ## confirm that a valid email and password return an API token
        response = self.client.post(
            reverse("api-login"),
            {
                "email": "apiowner@example.com",
                "password": "Test123!",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertIn(
            "token",
            response.data,
        )

    def test_unauthenticated_user_cannot_view_api_links(self):
        ## link management should only be available to logged-in users
        response = self.client.get(
            reverse("api-links")
        )

        self.assertEqual(
            response.status_code,
            401,
        )

    def test_authenticated_user_can_view_own_api_links(self):
        ## need the API to return the logged-in user's links, not every link in db
        self.authenticate_as_owner()

        response = self.client.get(
            reverse("api-links")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["label"],
            "API Owner GitHub",
        )

    def test_authenticated_user_can_create_api_link(self):
        ## check that a logged-in user can create a new profile link through the API
        self.authenticate_as_owner()

        response = self.client.post(
            reverse("api-links"),
            {
                "platform": "website",
                "label": "API Website",
                "url": "https://example.com",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        self.assertTrue(
            ProfileLink.objects.filter(
                profile=self.owner.profile,
                label="API Website",
            ).exists()
        )

    def test_authenticated_user_can_update_own_api_link(self):
        ## confirm that users can update their own links through patchh
        self.authenticate_as_owner()

        response = self.client.patch(
            reverse(
                "api-link-detail",
                args=[self.owner_link.id],
            ),
            {
                "label": "Updated API GitHub",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.owner_link.refresh_from_db()

        self.assertEqual(
            self.owner_link.label,
            "Updated API GitHub",
        )

    def test_user_cannot_update_another_users_api_link(self):
        ## check the ownership protection. user should not be able to edit a link owned by someone else.
        self.authenticate_as_owner()

        response = self.client.patch(
            reverse(
                "api-link-detail",
                args=[self.other_link.id],
            ),
            {
                "label": "Unauthorised Update",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_authenticated_user_can_delete_own_api_link(self):
        ## confirm that users can delete their own links through the API
        self.authenticate_as_owner()

        response = self.client.delete(
            reverse(
                "api-link-detail",

                args=[self.owner_link.id],
            )
        )

        self.assertEqual(
            response.status_code,
            204,
        )

        self.assertFalse(
            ProfileLink.objects.filter(
                id=self.owner_link.id,
            ).exists()
        )

    def test_api_visibility_get_returns_fields_and_links(self):
        ## visibility API to return both sections used by the website:
        ## profile field rules and profile link rules.
        self.authenticate_as_owner()

        response = self.client.get(
            reverse("api-visibility")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertIn(
            "profile_fields",
            response.data,
        )

        self.assertIn(
            "profile_links",
            response.data,
        )

    def test_api_visibility_patch_updates_rules(self):
        ## check that patch can update both profile field visibility and profile link visibility
        self.authenticate_as_owner()

        response = self.client.patch(
            reverse("api-visibility"),
            {
                "profile_fields": [
                    {
                        "field_name": "display_name",
                        "visible_to": [
                            "public",
                            "professional",

                        ],
                    }
                ],
                "profile_links": [
                    {
                        "link_id": self.owner_link.id,
                        "visible_to": [
                            "public",

                        ],
                    }
                ],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTrue(
            VisibilityRule.objects.filter(
                owner=self.owner,
                field_name="display_name",
                visible_to="public",
            ).exists()
        )

        self.assertTrue(
            VisibilityRule.objects.filter(
                owner=self.owner,
                field_name="display_name",
                visible_to="professional",
            ).exists()
        )

        self.assertTrue(
            LinkVisibilityRule.objects.filter(
                owner=self.owner,
                link=self.owner_link,
                visible_to="public",
            ).exists()
        )