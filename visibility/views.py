from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .constants import PROFILE_FIELDS
from .models import VisibilityRule


@login_required
def visibility_rules(request):
    if request.method == "POST":
        VisibilityRule.objects.filter(owner=request.user).delete()

    context = {
        "profile_fields": PROFILE_FIELDS,
    }

    return render(request, "visibility/rules.html", context)