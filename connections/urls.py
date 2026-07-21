from django.urls import path

from . import views

app_name = "connections"

urlpatterns = [
    path("search/", views.search_users, name="search_users"),
    path("request/<int:user_id>/", views.send_connection_request, name="send_connection_request",),
    path("pending/", views.pending_requests, name="pending_requests",),
    path("review/<int:connection_id>/", views.review_request, name="review_request",),
    path("", views.connections_list, name="connections_list",),
]