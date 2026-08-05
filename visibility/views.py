from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .constants import PROFILE_FIELDS
from .models import VisibilityRule
from connections.constants import RELATIONSHIP_TYPES

@login_required
def visibility_rules(request):

    if request.method == "POST":
        VisibilityRule.objects.filter(owner=request.user).delete()

        for field_name, _ in PROFILE_FIELDS:

            for relationship in RELATIONSHIP_TYPES:
                checkbox_name = f"{field_name}_{relationship}"

                if checkbox_name in request.POST:
                    VisibilityRule.objects.create(
                        owner=request.user,
                        field_name=field_name,
                        visible_to=relationship,
                    )

    saved_rules = VisibilityRule.objects.filter(owner=request.user)

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

    context = {
        "profile_fields": profile_fields,
    }

    return render(request, "visibility/rules.html", context)