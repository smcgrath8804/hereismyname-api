from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .constants import PROFILE_FIELDS
from .models import VisibilityRule


@login_required
def visibility_rules(request):

    RELATIONSHIP_TYPES = [
        "public",
        "professional",
        "personal",
        "general",
    ]

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

    context = {
        "profile_fields": PROFILE_FIELDS,
    }

    return render(request, "visibility/rules.html", context)