from django.urls import path

from .views import ProfileAPIView

urlpatterns = [

    path(
        "profile/<str:username>/",
        ProfileAPIView.as_view(),
        name="api-profile",
    ),

]