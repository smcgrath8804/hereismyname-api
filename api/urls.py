from django.urls import path

from .views import ProfileAPIView

from .views import MyProfileAPIView

urlpatterns = [

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

]