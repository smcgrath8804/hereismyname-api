from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .constants import PROFILE_FIELDS
from .models import VisibilityRule, LinkVisibilityRule
from connections.constants import RELATIONSHIP_TYPES

from links.models import ProfileLink


@login_required
def visibility_rules(request):

    if request.method == "POST":
        VisibilityRule.objects.filter(owner=request.user).delete()

        for field_name, _ in PROFILE_FIELDS:

            for relationship, _ in RELATIONSHIP_TYPES:

                checkbox_name = f"{field_name}_{relationship}"

                if checkbox_name in request.POST:
                    VisibilityRule.objects.create(
                        owner=request.user,
                        field_name=field_name,
                        visible_to=relationship,
                    )

    saved_rules = VisibilityRule.objects.filter(owner=request.user)

    saved_link_rules = LinkVisibilityRule.objects.filter(
        owner=request.user,
    )

    selected_links = {
        (rule.link_id, rule.visible_to)
        for rule in saved_link_rules
    }

    selected = {
        (rule.field_name, rule.visible_to)
        for rule in saved_rules
    }

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

    profile_links = []

    for link in ProfileLink.objects.filter(
            profile=request.user.profile,
    ):
        profile_links.append({

            "id": link.id,
            "title": (link.platform_name
                if link.platform == "other"
                else link.get_platform_display()
            ),
            "label": link.label,
            "url": link.url,
            "public": (link.id, "public", ) in selected_links,
            "professional": (link.id, "professional", ) in selected_links,
            "personal": (link.id, "personal", ) in selected_links,
            "general": (link.id, "general", ) in selected_links,
        })

    context = {

        "profile_fields": profile_fields,
        "profile_links": profile_links,

    }

    return render(request, "visibility/rules.html", context)