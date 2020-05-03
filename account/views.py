""" Imports """

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import ConnexionForm, UserUpdateForm, SignUpForm
from home.forms import SearchForm
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from substitute.models import Substitute, Family
from django.contrib.auth.decorators import login_required


@login_required
def favorites(request, id_family=None):
    """
    @require login
    Views for favorites
    :param request:
    :return render favorites.html:
    """
    family = None
    if request.method == "GET" and id_family != None:
        if id_family != 0:
            family = Family.objects.get(pk=id_family)
            favoris = Substitute.objects.filter(user_id=request.user, family_id=family)
        else:
            favoris = Substitute.objects.filter(user_id=request.user)
    else:
        favoris = Substitute.objects.filter(user_id=request.user)

    a = len(favoris)

    families = Family.objects.all()
    return render(
        request,
        "favorites.html",
        {
            "title": "Mes favoris",
            "favoris": favoris,
            "families": families,
            "family": family,
            "form_search": SearchForm(None),
        },
    )


@login_required
def save_favorites(request, id_favori, id_family):
    """
        @require login
        Views for favorites
        :param request:
        :return render favorites.html:
    """

    if request.method == "GET":
        favori = Substitute.objects.get(pk=id_favori)
        if id_family == 0:
            family = None
        else:
            family = Family.objects.get(pk=id_family, user_id=request.user)
        favori.family_id = family
        favori.save()

    return redirect(reverse("account:favorites"))


@login_required
def save_family(request, family_name=None):
    """
        @require login
        Views for favorites
        :param request:
        :return render favorites.html:
    """

    if (
        request.method == "GET"
        and family_name != None
        and not Family.objects.filter(name=family_name, user_id=request.user).exists()
    ):
        family = Family.objects.create(name=family_name, user_id=request.user)
        family.save()

    return redirect(reverse("account:favorites"))


@login_required
def profile(request):
    """
    @require login
    Views for profile
    :param request:
    :return render profile.html:
    """

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        try:
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    "Les modifications de votre profil ont bien été enregistrées",
                )
        except:  # pragma: no cover
            messages.error(
                request,
                "Erreurs durant l'enregistrement des informations de votre profil",
            )
    else:
        form = UserUpdateForm(instance=request.user)

    return render(
        request, "profile.html", {"form": form, "form_search": SearchForm(None)}
    )


def login(request):
    """
    Views for login
    :param request:
    :return
    if method post and login ok
        if previous page exist : render last visited page
        else: render home.html
    else
        render login.html
    :
    """
    if request.user.is_authenticated:
        return redirect(reverse("home:index"))
    else:
        if request.method == "POST":
            form = ConnexionForm(data=request.POST)
            try:
                if form.is_valid():
                    user = authenticate(
                        username=form.cleaned_data["username"],
                        password=form.cleaned_data["password"],
                    )
                    try:
                        if user:
                            auth_login(request, user)
                            request.session.set_expiry(900)
                            return HttpResponseRedirect(request.session["previous"])
                        else:
                            messages.error(request, "Mauvais login/mot de passe.")
                            return render(request, "login.html", {"form": form})
                    except:  # pragma: no cover
                        redirect(reverse("home:index"))
            except Exception as e:  # pragma: no cover
                messages.error(request, "Erreur de login.")
                return render(request, "login.html", {"form": form})
        else:
            form = ConnexionForm(None)
            request.session["previous"] = request.META.get("HTTP_REFERER")

        return render(
            request, "login.html", {"form": form, "form_search": SearchForm(None)}
        )


def register(request):
    """
    Views for register
    :param request:
    :return
    if method post and form valid
        create user, login and redirect to home.html
    else
        render register.html
    :
    """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password1")
                user = authenticate(username=username, password=raw_password)
                auth_login(request, user)
                return redirect(reverse("home:index"))

        except Exception as e:
            messages.error(request, "Votre compte n'a pas été crée.")
    else:
        form = SignUpForm(None)

    return render(
        request, "register.html", {"form": form, "form_search": SearchForm(None)}
    )


@login_required
def logout(request):
    """
    @require login
    Views for logout
    :param request:
    :return reditrect to home.html:
    """
    auth_logout(request)
    return redirect(reverse("home:index"))
