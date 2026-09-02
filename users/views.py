from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm

from django.contrib.auth import login


def register(request):
    ## Register a new user then log them in automatically
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")

    else:
        form = RegisterForm()

    return render(request, "users/register.html", {
        "form": form,
    })

@login_required
def dashboard(request):
    ## Show the logged-in users dashboard
    return render(
        request,
        "users/dashboard.html",
        {
            "profile": request.user.profile,
        },
    )