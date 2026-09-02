from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileLinkForm

from .models import ProfileLink

from .services import get_user_link_or_404, get_user_links


@login_required
def links_list(request):
    ## Show all profile links owned by the logged-in user
    links = get_user_links(
        request.user,
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
    ## Add a new profile link or edit an existing one
    if link_id:

        link = get_user_link_or_404(
            request.user,
            link_id,
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
                    get_user_links(
                        request.user,
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
    ## Delete one profile link owned by the logged-in user
    link = get_user_link_or_404(
        request.user,
        link_id,
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