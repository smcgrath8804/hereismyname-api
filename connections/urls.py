from django.urls import path

from . import views

app_name = "connections"

urlpatterns = [
    path("search/", views.search_users, name="search_users"),
]