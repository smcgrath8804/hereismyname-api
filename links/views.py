from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileLinkForm
from .models import ProfileLink


@login_required
def links_list(request):

    links = ProfileLink.objects.filter(
        profile=request.user.profile,
    )

    return render(
        request,
        "links/links_list.html",
        {
            "links": links,
        },
    )


@login_required
def link_form(request, link_id=None):

    if link_id:

        link = get_object_or_404(
            ProfileLink,
            id=link_id,
            profile=request.user.profile,
        )

    else:

        link = None

    if request.method == "POST":

        form = ProfileLinkForm(
            request.POST,
            instance=link,
        )

        if form.is_valid():

            new_link = form.save(
                commit=False,
            )

            if link is None:

                new_link.profile = request.user.profile

                new_link.display_order = (
                    ProfileLink.objects.filter(
                        profile=request.user.profile,
                    ).count()
                )

                messages.success(
                    request,
                    "Link added successfully.",
                )

            else:

                messages.success(
                    request,
                    "Link updated successfully.",
                )

            new_link.save()

            return redirect(
                "links:links_list",
            )

    else:

        form = ProfileLinkForm(
            instance=link,
        )

    return render(
        request,
        "links/link_form.html",
        {
            "form": form,
            "link": link,
        },
    )


@login_required
def delete_link(request, link_id):

    link = get_object_or_404(
        ProfileLink,
        id=link_id,
        profile=request.user.profile,
    )

    if request.method == "POST":

        link.delete()

        messages.success(
            request,
            "Link deleted successfully.",
        )

        return redirect(
            "links:links_list",
        )

    return render(
        request,
        "links/delete_link.html",
        {
            "link": link,
        },
    )