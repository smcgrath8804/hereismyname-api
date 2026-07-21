from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Connection

User = get_user_model()


@login_required
def search_users(request):
    query = request.GET.get("q", "")
    users = []

    if query:
        users = User.objects.filter(
            username__icontains=query
        ).exclude(id=request.user.id)

    context = {
        "query": query,
        "users": users,
    }

    return render(request, "connections/search_users.html", context)

@login_required
def send_connection_request(request, user_id):

    if request.method != "POST":
        return redirect("connections:search_users")

    owner = get_object_or_404(User, id=user_id)

    if owner == request.user:
        messages.error(request, "You cannot send a connection request to yourself.")
        return redirect("connections:search_users")

    Connection.objects.get_or_create(
        owner=owner,
        requester=request.user,
    )

    messages.success(request, "Connection request sent.")

    return redirect("connections:search_users")