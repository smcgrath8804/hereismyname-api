def build_connection_data(connection):
    """ Build a consistent API representation of a connection for re-use """

    return {
        "id": connection.id,
        "username": connection.requester.username,
        "display_name": connection.requester.profile.display_name,
        "relationship": connection.relationship,
    }