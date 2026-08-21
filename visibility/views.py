from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from connections.constants import RELATIONSHIP_TYPES
from links.models import ProfileLink
from .constants import PROFILE_FIELDS
from .models import VisibilityRule, LinkVisibilityRule


@login_required
def visibility_rules(request):
    ## Save the submitted visibility rules
    if request.method == "POST":

        ## Remove existing rules before recreate them
        VisibilityRule.objects.filter(owner=request.user,).delete()

        LinkVisibilityRule.objects.filter(
            owner=request.user,
        ).delete()


        ## Save profile field visibility
        for field_name, _ in PROFILE_FIELDS:
            for relationship, _ in RELATIONSHIP_TYPES:
                checkbox_name = (
                    f"{field_name}_{relationship}"
                )

                if checkbox_name in request.POST:
                    VisibilityRule.objects.create(
                        owner=request.user,
                        field_name=field_name,
                        visible_to=relationship,
                    )


        ## Save profile link visibility
        for link in ProfileLink.objects.filter(
            profile=request.user.profile,
        ):

            for relationship, _ in RELATIONSHIP_TYPES:

                checkbox_name = (
                    f"link_{link.id}_{relationship}"
                )

                if checkbox_name in request.POST:

                    LinkVisibilityRule.objects.create(
                        owner=request.user,
                        link=link,
                        visible_to=relationship,
                    )


    ## Load the saved visibility rules
    saved_rules = VisibilityRule.objects.filter(
        owner=request.user,
    )

    saved_link_rules = LinkVisibilityRule.objects.filter(
        owner=request.user,
    )

    ## Create sets to help wih fast checking
    selected = {
        (rule.field_name, rule.visible_to)
        for rule in saved_rules
    }

    selected_links = {
        (rule.link_id, rule.visible_to)
        for rule in saved_link_rules
    }


    ## Build the profile field data
    profile_fields = []

    for field_name, field_label in PROFILE_FIELDS:
        profile_fields.append({
            "name": field_name,
            "label": field_label,

            "public": (field_name, "public") in selected,
            "professional": (field_name, "professional") in selected,
            "personal": (field_name, "personal") in selected,
            "general": (field_name, "general") in selected,
        })


    ## Build the profile link data
    profile_links = []

    for link in ProfileLink.objects.filter(
        profile = request.user.profile,
    ):

        profile_links.append({
            "id": link.id,
            "title": (
                link.platform_name
                if link.platform == "other"
                else link.get_platform_display()
            ),
            "label": link.label,
            "url": link.url,

            "public": (link.id, "public") in selected_links,
            "professional": (link.id, "professional") in selected_links,
            "personal": (link.id, "personal") in selected_links,
            "general": (link.id, "general") in selected_links,

        })

    ## Render the page
    context = {

        "profile_fields": profile_fields,
        "profile_links": profile_links,

    }
    return render(
        request,
        "visibility/rules.html",
        context,
    )