from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileForm
from .models import Profile
from connections.models import Connection
from visibility.models import VisibilityRule


def profile_view(request, username):

    profile = get_object_or_404(
        Profile,
        user__username=username
    )

    visible_fields = {}

    if request.user.is_authenticated and request.user == profile.user:

        visible_fields = {
            "display_name": profile.display_name,
            "local_language_name": profile.local_language_name,
            "email": profile.email,
            "phone": profile.phone,
            "job_title": profile.job_title,
            "company": profile.company,
            "bio": profile.bio,
        }

    else:

        if request.user.is_authenticated:

            try:

                connection = Connection.objects.get(
                    owner=profile.user,
                    requester=request.user
                )

                rules = VisibilityRule.objects.filter(
                    owner=profile.user,
                    visible_to=connection.relationship
                )

                for rule in rules:
                    visible_fields[rule.field_name] = getattr(
                        profile,
                        rule.field_name
                    )


            except Connection.DoesNotExist:

                rules = VisibilityRule.objects.filter(

                    owner=profile.user,

                    visible_to="public"

                )

                for rule in rules:
                    visible_fields[rule.field_name] = getattr(

                        profile,

                        rule.field_name

                    )

        else:

            rules = VisibilityRule.objects.filter(
                owner=profile.user,
                visible_to="public"
            )

            for rule in rules:
                visible_fields[rule.field_name] = getattr(
                    profile,
                    rule.field_name
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