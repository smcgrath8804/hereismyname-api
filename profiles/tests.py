from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from connections.models import Connection
from links.models import ProfileLink
from visibility.models import VisibilityRule, LinkVisibilityRule

User = get_user_model()

class ProfilePageTests(TestCase):
    """
    ### References used: Django testing tools:
    ## https://docs.djangoproject.com/en/6.0/topics/testing/tools/

    ## Django URL reversing:
    ## https://docs.djangoproject.com/en/6.0/ref/urlresolvers/
    """

    def setUp(self):
        ## create an owner and a viewer
        self.owner = User.objects.create_user(
            username="profileowner",
            email="profileowner@example.com",
            password="Test123!",
        )

        self.viewer = User.objects.create_user(
            username="profileviewer",
            email="profileviewer@example.com",
            password="Test123!",
        )

        ## add sample profile data so the tests can check which fields appear
        self.profile = self.owner.profile
        self.profile.display_name = "Profile Owner"
        self.profile.email = "profileowner@example.com"
        self.profile.phone = "123456789"
        self.profile.job_title = "Software Developer"
        self.profile.company = "Example Company"
        self.profile.bio = "This is the public profile bio."
        self.profile.save()

        ## reate two links to test link visibility on the profile page

        self.public_link = ProfileLink.objects.create(
            profile=self.owner.profile,
            platform="website",
            label="Public Website",
            url="https://example.com/public",
            display_order=0,
        )

        self.professional_link = ProfileLink.objects.create(
            profile=self.owner.profile,
            platform="github",
            label="Professional GitHub",
            url="https://github.com/profileowner",
            display_order=1,
        )

    def test_profile_page_loads_for_existing_user(self):
        ## confirm that a valid profile username opens the profile page
        response = self.client.get(
            reverse(
                "profiles:profile",
                args=[self.owner.username],
            )
        )
        self.assertEqual(
            response.status_code,
            200,
        )

    def test_profile_page_returns_404_for_missing_user(self):
        ## confirm that the app does not crash if a profile is missing
        response = self.client.get(
            reverse(
                "profiles:profile",
                args=["missinguser"],
            )
        )
        self.assertEqual(
            response.status_code,
            404,
        )

    def test_profile_owner_can_see_own_profile_data(self):
        ## need the profile owner to see their own full profile even before visibility rules have been created
        self.client.login(
            email="profileowner@example.com",
            password="Test123!",
        )
        response = self.client.get(
            reverse(
                "profiles:profile",
                args=[self.owner.username],
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "Profile Owner",
        )

        self.assertContains(
            response,
            "profileowner@example.com",
        )

        self.assertContains(
            response,
            "Software Developer",
        )

        self.assertContains(
            response,
            "Public Website",
        )

        self.assertContains(
            response,
            "Professional GitHub",
        )

    def test_public_viewer_only_sees_public_profile_data(self):
        ## check the baseline public view. The viewer is not connected, so should only see public fields and links
        VisibilityRule.objects.create(
            owner=self.owner,
            field_name="display_name",
            visible_to="public",
        )

        VisibilityRule.objects.create(
            owner=self.owner,
            field_name="bio",
            visible_to="public",
        )

        LinkVisibilityRule.objects.create(
            owner=self.owner,
            link=self.public_link,
            visible_to="public",
        )

        response = self.client.get(
            reverse(
                "profiles:profile",
                args=[self.owner.username],
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "Profile Owner",
        )
        self.assertContains(
            response,
            "This is the public profile bio.",
        )


        self.assertContains(
            response,
            "Public Website",
        )

        self.assertNotContains(
            response,
            "profileowner@example.com",
        )

        self.assertNotContains(
            response,
            "Software Developer",
        )

        self.assertNotContains(
            response,
            "Professional GitHub",
        )

    def test_professional_connection_sees_public_and_professional_data(self):
        ## check the main context-aware behaviour. A professional connection will see public and professional information
        Connection.objects.create(
            owner=self.owner,
            requester=self.viewer,
            relationship="professional",
        )

        VisibilityRule.objects.create(
            owner=self.owner,
            field_name="display_name",
            visible_to="public",
        )

        VisibilityRule.objects.create(
            owner=self.owner,
            field_name="job_title",
            visible_to="professional",
        )

        VisibilityRule.objects.create(
            owner=self.owner,
            field_name="company",
            visible_to="professional",
        )

        LinkVisibilityRule.objects.create(
            owner=self.owner,
            link=self.public_link,
            visible_to="public",
        )

        LinkVisibilityRule.objects.create(
            owner=self.owner,
            link=self.professional_link,
            visible_to="professional",
        )

        self.client.login(
            email="profileviewer@example.com",
            password="Test123!",
        )

        response = self.client.get(
            reverse(
                "profiles:profile",
                args=[self.owner.username],
            )
        )


        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "Profile Owner",
        )

        self.assertContains(
            response,
            "Software Developer",
        )

        self.assertContains(
            response,
            "Example Company",
        )

        self.assertContains(
            response,
            "Public Website",
        )

        self.assertContains(
            response,
            "Professional GitHub",
        )

        self.assertNotContains(
            response,
            "profileowner@example.com",
        )


        self.assertNotContains(
            response,
            "123456789",
        )