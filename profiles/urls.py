from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    ## ==== Edit profile ====
    path("edit/", views.edit_profile, name="edit_profile"),

    ## ==== View profile ====
    path("<str:username>/", views.profile_view, name="profile"),
]