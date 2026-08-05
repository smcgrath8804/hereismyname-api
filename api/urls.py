from django.urls import path

from .views import (LoginAPIView, MyProfileAPIView, ProfileAPIView,
                    ConnectionsAPIView, ConnectionDetailAPIView, PendingConnectionsAPIView)

urlpatterns = [

    path(
        "login/",
        LoginAPIView.as_view(),
        name="api-login",
    ),
    
    path(
        "profile/me/",
        MyProfileAPIView.as_view(),
        name="api-my-profile",
    ),

    path(
        "profile/<str:username>/",
        ProfileAPIView.as_view(),
        name="api-profile",
    ),

    path(
        "connections/",
        ConnectionsAPIView.as_view(),
        name="api-connections",
    ),

    path(
        "connections/<int:connection_id>/",
        ConnectionDetailAPIView.as_view(),
        name="api-connection-detail",
    ),

    path(
        "pending/",
        PendingConnectionsAPIView.as_view(),
        name="api-pending-connections",
    ),

]