"""Contains the application’s url."""
from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.home, name="index"),
    path("mentions/", views.mentions, name="mentions"),
    path("product/", views.search, name="search"),
    path("product/<int:order>/", views.search, name="search"),
    path("product/<int:order>/?page=<int:page>", views.search, name="search"),
    path("product/?page=<int:page>", views.search, name="search"),
]
