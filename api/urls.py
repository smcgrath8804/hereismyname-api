from django.urls import path

from .views import (LoginAPIView, MyProfileAPIView, ProfileAPIView, ConnectionsAPIView)

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

]