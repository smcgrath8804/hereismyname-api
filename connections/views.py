from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages


from .models import Connection
from .services import (create_connection_request, review_connection_request,)
from .constants import RELATIONSHIP_TYPES

User = get_user_model()

## Search for other users and show existing sent requests
@login_required
def search_users(request):
    query = request.GET.get("q", "")
    users = []

    if query:
        users = User.objects.filter(
            username__icontains=query
        ).exclude(
            id=request.user.id
        ).exclude(
            is_superuser=True
        ).exclude(
            username="admin"
        )

        existing_requests = Connection.objects.filter(
            requester=request.user,
            owner__in=users,
        )

        requested_user_ids = set(
            existing_requests.values_list("owner_id", flat=True)
        )

    context = {
        "query": query,
        "users": users,
        "requested_user_ids": requested_user_ids if query else set(),
    }

    return render(request, "connections/search_users.html", context)

## Create a new pending connection request
@login_required
def send_connection_request(request, user_id):

    if request.method != "POST":
        return redirect("connections:search_users")

    owner = get_object_or_404(User, id=user_id)

    try:
        connection, created = create_connection_request(
            owner,
            request.user,
        )

    except ValueError as error:
        messages.error(request, str(error))

        return redirect("connections:search_users")

    if created:
        messages.success(request, "Connection request sent.")

    else:
        messages.info(request, "Connection request already exists.")

    return redirect("connections:search_users")

## Accept a pending connection request
@login_required
def review_request(request, connection_id):

    if request.method != "POST":
        return redirect("connections:connections_list")

    connection = get_object_or_404(
        Connection,
        id=connection_id,
        owner=request.user,
        relationship__isnull=True,
    )

    relationship = request.POST.get("relationship")

    try:
        review_connection_request(
            connection,
            relationship,
        )

        messages.success(
            request,
            "Connection updated successfully."
        )

    except ValueError as error:
        messages.error(
            request,
            str(error),
        )

    return redirect("connections:connections_list")

## Show sent, pending and accepted connections
@login_required
def connections_list(request):

    if request.method == "POST":

        connection = get_object_or_404(
            Connection,
            id=request.POST.get("connection_id"),
            owner=request.user,
            relationship__isnull=False,
        )

        relationship = request.POST.get("relationship")

        try:

            review_connection_request(
                connection,
                relationship,
            )

            messages.success(
                request,
                "Connection updated successfully."
            )

        except ValueError as error:

            messages.error(
                request,
                str(error),
            )

        return redirect("connections:connections_list")

    received_connections = Connection.objects.filter(
        owner=request.user,
        relationship__isnull=False,
    ).order_by("requester__username")

    sent_requests = Connection.objects.filter(
        requester=request.user,
    ).order_by("owner__username")

    pending_requests = Connection.objects.filter(
        owner=request.user,
        relationship__isnull=True,
    ).order_by("requester__username")

    return render(
        request,
        "connections/connections_list.html",
        {
            "sent_requests": sent_requests,
            "pending_requests": pending_requests,
            "received_connections": received_connections,
            "relationship_types": RELATIONSHIP_TYPES,
        },
    )