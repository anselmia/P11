from django.shortcuts import render, redirect
from home import search
from .models import Substitute, Family
from home.models import Product
from home.forms import SearchForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse


def substitute(request, product_id):
    if request.method == "GET":
        substitutes = search.search_substitute(product_id)
        if substitutes.count() > 0:
            paginator = Paginator(substitutes, 6)
            page = request.GET.get("page")
            substitutes = paginator.get_page(page)
            context = {}
            context["substitutes"] = substitutes
            context["title"] = "Substituts"
            context["product"] = Product.objects.get(pk=product_id)
            context["form_search"] = SearchForm(None)

            return render(request, "substitute.html", context)
        else:
            messages.warning(request, "Il n'y a pas de substitut pour ce produit")
            return redirect("home:index")


def detail(request, product_id, substitute_id):
    if request.method == "GET":
        try:
            substitute = Product.objects.get(pk=substitute_id)
            product = Product.objects.get(pk=product_id)
            if substitute is not None:
                context = {}
                context["product"] = product
                context["substitute"] = substitute
                context["title"] = "Détails du produit " + substitute.name
                if request.user.is_authenticated:
                    context["exist"] = Substitute.objects.filter(
                        user_id=request.user,
                        product_id=product,
                        substitute_id=substitute,
                    ).exists()
                context["form_search"] = SearchForm(None)

                return render(request, "detail.html", context)
            else:
                messages.warning(
                    request,
                    "Il y a eu une lors de la récupération des information du substitut",
                )
                return render(request, "home.html", {"form_search": SearchForm(None)})
        except:  # pragma: no cover
            messages.warning(
                request,
                "Il y a eu une lors de la récupération des information du substitut",
            )
            return render(request, "home.html", {"form_search": SearchForm(None)})


@login_required
def save(request, product_id, substitute_id):
    if request.method == "GET" and product_id and substitute_id:
        substitute = Product.objects.get(pk=substitute_id)
        product = Product.objects.get(pk=product_id)
        context = {}
        context["product"] = product
        context["substitute"] = substitute
        context["title"] = "Détails du produit " + substitute.name
        try:
            user_product = Substitute(
                user_id=request.user, product_id=product, substitute_id=substitute
            )
            user_product.save()
            messages.success(request, "Votre substitut a été sauvé")
            context["exist"] = True

        except:  # pragma: no cover
            messages.warning(request, "Erreur lors de l'enregistrement du favoris")

        context["form_search"] = SearchForm(None)
        return render(request, "detail.html", context)


@login_required
def detail_favoris(request, product_id, substitute_id):
    if request.method == "GET":
        context = {}
        context["form_search"] = SearchForm(None)
        substitute = Product.objects.get(pk=substitute_id)
        families = Family.objects.all()
        product = Product.objects.get(pk=product_id)
        if substitute is not None and product is not None:
            context["product"] = product
            context["substitute"] = substitute
            context["title"] = "Détails du favoris"
            context["families"] = families
            return render(request, "detail_favoris.html", context)
        else:  # pragma: no cover
            messages.warning(
                request,
                "Il y a eu une erreur lors de la récupération des informations du favoris",
            )
            return redirect(reverse('home:index'))
