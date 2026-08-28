from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import ProfileLink


User = get_user_model()


class ProfileLinkViewTests(TestCase):
    """Tests using Django's built-in TestCase and test client.
    https://docs.djangoproject.com/en/6.0/topics/testing/tools/"""

    def setUp(self):
        # Create two users so the tests can check link ownership
        self.owner = User.objects.create_user(
            username="linkowner",
            email="linkowner@example.com",
            password="Test123!",
        )

        self.other_user = User.objects.create_user(
            username="otherlinkuser",
            email="otherlinkuser@example.com",
            password="Test123!",
        )

        # Links belonging to the logged-in test user
        self.owner_link = ProfileLink.objects.create(
            profile=self.owner.profile,
            platform="github",
            label="Owner GitHub",
            url="https://github.com/linkowner",
            display_order=0,
        )

        # Link belonging to another user.
        self.other_link = ProfileLink.objects.create(
            profile=self.other_user.profile,
            platform="linkedin",
            label="Other LinkedIn",
            url="https://linkedin.com/in/otherlinkuser",
            display_order=0,
        )

    def test_logged_in_user_can_view_my_links_page(self):
        # The owner should be able to open their own links page
        self.client.login(
            email="linkowner@example.com",
            password="Test123!",
        )

        response = self.client.get(
            reverse("links:links_list")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "Owner GitHub",
        )

    def test_anonymous_user_is_redirected_from_links_page(self):
        # Anonymous visitors should be redirected away from the link management
        response = self.client.get(
            reverse("links:links_list")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_logged_in_user_can_create_link(self):
        # A logged-in user should be able to add a new profile link
        self.client.login(
            email="linkowner@example.com",
            password="Test123!",
        )

        response = self.client.post(
            reverse("links:add_link"),
            {
                "platform": "website",
                "platform_name": "",
                "label": "Personal Website",
                "url": "https://example.com",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertTrue(
            ProfileLink.objects.filter(
                profile=self.owner.profile,
                label="Personal Website",
            ).exists()
        )

    def test_logged_in_user_can_update_own_link(self):
        # User should be able to edit a link that belongs to them
        self.client.login(
            email="linkowner@example.com",
            password="Test123!",
        )

        response = self.client.post(
            reverse(
                "links:edit_link",
                args=[self.owner_link.id],
            ),
            {
                "platform": "github",
                "platform_name": "",
                "label": "Updated GitHub",
                "url": "https://github.com/updated-linkowner",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.owner_link.refresh_from_db()

        self.assertEqual(
            self.owner_link.label,
            "Updated GitHub",
        )

    def test_user_cannot_update_another_users_link(self):
        # Ownership filter to stop users editing links they do not own
        self.client.login(
            email="linkowner@example.com",
            password="Test123!",
        )

        response = self.client.post(
            reverse(
                "links:edit_link",
                args=[self.other_link.id],
            ),
            {
                "platform": "linkedin",
                "platform_name": "",
                "label": "Changed By Wrong User",
                "url": "https://example.com/not-allowed",
            },
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_logged_in_user_can_delete_own_link(self):
        # A user should be able to delete a link that belongs to them
        self.client.login(
            email="linkowner@example.com",
            password="Test123!",
        )

        response = self.client.post(
            reverse(
                "links:delete_link",
                args=[self.owner_link.id],
            )
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertFalse(
            ProfileLink.objects.filter(
                id=self.owner_link.id,
            ).exists()
        )

    def test_user_cannot_delete_another_users_link(self):
        # Ownership filter to stop users deleting links they do not own
        self.client.login(
            email="linkowner@example.com",
            password="Test123!",
        )

        response = self.client.post(
            reverse(
                "links:delete_link",
                args=[self.other_link.id],
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )

        self.assertTrue(
            ProfileLink.objects.filter(
                id=self.other_link.id,
            ).exists()
        )