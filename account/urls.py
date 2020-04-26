"""Contains the application’s url."""
from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("favorites/", views.favorites, name="favorites"),
    path("favorites/<int:id_family>/", views.favorites, name="favorites"),
    path("save_family/<slug:family_name>/", views.save_family, name="save_family"),
    path(
        "save_favorites/<int:id_favori>/<int:id_family>/",
        views.save_favorites,
        name="save_favorites",
    ),
    path("register/", views.register, name="register"),
]
