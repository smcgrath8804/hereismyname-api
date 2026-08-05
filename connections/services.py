from .models import Connection

def build_connection_data(connection):
    """ Build a consistent API representation of a connection for re-use """

    return {
        "id": connection.id,
        "username": connection.requester.username,
        "display_name": connection.requester.profile.display_name,
        "relationship": connection.relationship,
    }

def build_pending_connection_data(connection):
    """ Build a consistent API representation of a pending connection request. """

    return {
        "id": connection.id,
        "username": connection.requester.username,
        "display_name": connection.requester.profile.display_name,
    }

def create_connection_request(owner, requester):
    """ Create a connection request if one does not already exist. """

    if owner == requester:
        raise ValueError(
            "You can't send a connection request to yourself."
        )

    connection, created = Connection.objects.get_or_create(
        owner=owner,
        requester=requester,
    )
    return connection, created