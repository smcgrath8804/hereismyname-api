from django.urls import path
from . import views

urlpatterns = [
    path("", views.visibility_rules, name="visibility_rules"),
]