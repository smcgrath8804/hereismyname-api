from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileForm
from .models import Profile
from .services import get_visible_fields


def profile_view(request, username):

    profile = get_object_or_404(
        Profile,
        user__username=username
    )

    visible_fields = get_visible_fields(
        profile,
        request.user
    )

    return render(
        request,
        "profiles/profile.html",
        {
            "profile": profile,
            "visible_fields": visible_fields
        }
    )


@login_required
def edit_profile(request):

    profile = request.user.profile

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            return redirect("dashboard")

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        "profiles/edit_profile.html",
        {
            "form": form
        }
    )