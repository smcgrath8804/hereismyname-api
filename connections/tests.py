from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from .models import Connection

User = get_user_model()


class ConnectionModelTests(TestCase):
    """
    References:
    Django testing tools: https://docs.djangoproject.com/en/6.0/topics/testing/tools/

    Django model unique constraints: https://docs.djangoproject.com/en/6.0/ref/models/options/#unique-together
    """

    def setUp(self):
        ## Create two users to test a connection between them
        self.owner = User.objects.create_user(
            username="connectionowner",
            email="connectionowner@example.com",
            password="Test123!",
        )

        self.requester = User.objects.create_user(
            username="connectionrequester",
            email="connectionrequester@example.com",
            password="Test123!",
        )

    def test_pending_connection_can_be_created(self):
        ## new connection request to be pending when no relationship selected
        connection = Connection.objects.create(
            owner=self.owner,
            requester=self.requester,
            relationship=None,
        )

        self.assertIsNone(
            connection.relationship,
        )

        self.assertEqual(
            str(connection),
            "connectionrequester@example.com to connectionowner@example.com (Pending)",
        )

    def test_accepted_connection_stores_relationship_type(self):
        ## after reviewed connection should store selected relationship type
        connection = Connection.objects.create(
            owner=self.owner,
            requester=self.requester,
            relationship="professional",
        )

        self.assertEqual(
            connection.relationship,
            "professional",
        )

        self.assertEqual(
            str(connection),
            "connectionrequester@example.com to connectionowner@example.com (professional)",
        )

    def test_duplicate_connection_between_same_users_is_blocked(self):
        ## model should not allow the same connection request to the same owner twice
        Connection.objects.create(
            owner=self.owner,
            requester=self.requester,
            relationship=None,
        )

        with self.assertRaises(IntegrityError):

            with transaction.atomic():

                Connection.objects.create(
                    owner=self.owner,
                    requester=self.requester,
                    relationship=None,
                )