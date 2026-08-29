from django.test import TestCase
from django.contrib.auth import get_user_model
from visibility.models import LinkVisibilityRule
from connections.models import Connection
from links.models import ProfileLink
from links.services import get_visible_links

User = get_user_model()

"""
Django testing tools: https://docs.djangoproject.com/en/6.0/topics/testing/tools/

Django model queries: https://docs.djangoproject.com/en/6.0/topics/db/queries/

Django many-object filtering with __in: https://docs.djangoproject.com/en/6.0/ref/models/querysets/#in
"""

class VisibilityRulesTests(TestCase):
    def setUp(self):
        ## Create two test users
        self.owner = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="Test123!",
        )
        self.viewer = User.objects.create_user(
            username="viewer",
            email="viewer@example.com",
            password="Test123!",
        )

        ## Get the owner's auto-created profile and add sample data.
        self.profile = self.owner.profile

        self.profile.display_name = "Owner Display Name"
        self.profile.email = "owner@example.com"
        self.profile.phone = "123456789"
        self.profile.job_title = "Software Developer"
        self.profile.company = "Example Company"
        self.profile.bio = "This is the owner's bio."

        self.profile.save()

    def test_owner_can_see_all_profile_links(self):
        ## owner should see all own links
        public_link = ProfileLink.objects.create(
            profile=self.owner.profile,
            platform="website",
            label="Public Website",
            url="https://example.com/public",
            display_order=0,
        )

        professional_link = ProfileLink.objects.create(
            profile=self.owner.profile,
            platform="github",
            label="Professional GitHub",
            url="https://github.com/owner",
            display_order=1,
        )

        visible_links = get_visible_links(
            self.owner.profile,
            self.owner,
        )
        self.assertIn(
            public_link,
            visible_links,
        )
        self.assertIn(
            professional_link,
            visible_links,
        )


    def test_public_viewer_only_sees_public_links(self):
        ## public viewer to only see links marked as public
        public_link = ProfileLink.objects.create(
            profile=self.owner.profile,
            platform="website",
            label="Public Website",
            url="https://example.com/public",
            display_order=0,
        )

        professional_link = ProfileLink.objects.create(
            profile=self.owner.profile,
            platform="github",
            label="Professional GitHub",
            url="https://github.com/owner",
            display_order=1,
        )

        LinkVisibilityRule.objects.create(
            owner=self.owner,
            link=public_link,
            visible_to="public",
        )

        visible_links = get_visible_links(
            self.owner.profile,
            self.viewer,
        )
        self.assertIn(
            public_link,
            visible_links,
        )
        self.assertNotIn(
            professional_link,
            visible_links,
        )


    def test_professional_connection_sees_public_and_professional_links(self):
        ## professional connection should see public links and professional links
        Connection.objects.create(
            owner=self.owner,
            requester=self.viewer,
            relationship="professional",
        )

        public_link = ProfileLink.objects.create(
            profile=self.owner.profile,
            platform="website",
            label="Public Website",
            url="https://example.com/public",
            display_order=0,
        )

        professional_link = ProfileLink.objects.create(
            profile=self.owner.profile,
            platform="github",
            label="Professional GitHub",
            url="https://github.com/owner",
            display_order=1,
        )

        personal_link = ProfileLink.objects.create(
            profile=self.owner.profile,
            platform="instagram",
            label="Personal Instagram",
            url="https://instagram.com/owner",
            display_order=2,
        )

        LinkVisibilityRule.objects.create(
            owner=self.owner,
            link=public_link,
            visible_to="public",
        )

        LinkVisibilityRule.objects.create(
            owner=self.owner,
            link=professional_link,
            visible_to="professional",
        )

        LinkVisibilityRule.objects.create(
            owner=self.owner,
            link=personal_link,
            visible_to="personal",
        )

        visible_links = get_visible_links(
            self.owner.profile,
            self.viewer,
        )

        self.assertIn(
            public_link,
            visible_links,
        )

        self.assertIn(
            professional_link,
            visible_links,
        )

        self.assertNotIn(
            personal_link,
            visible_links,
        )