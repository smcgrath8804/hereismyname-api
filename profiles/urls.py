from django.urls import path
from . import views

urlpatterns = [
    path("<int:profile_id>/", views.profile_view, name="profile"),
]