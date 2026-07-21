from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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
