from django.urls import path

from . import views


app_name = "links"

urlpatterns = [

    path(
        "",
        views.links_list,
        name="links_list",
    ),

    path(
        "add/",
        views.link_form,
        name="add_link",
    ),

    path(
        "<int:link_id>/edit/",
        views.link_form,
        name="edit_link",
    ),

    path(
        "<int:link_id>/delete/",
        views.delete_link,
        name="delete_link",
    ),

]