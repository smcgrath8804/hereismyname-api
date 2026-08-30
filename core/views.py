from django.shortcuts import redirect, render

def home(request):
    ## Send logged-in users straight to their own dashboard
    if request.user.is_authenticated:
        return redirect("dashboard")

    return render(
        request,
        "home.html",
    )