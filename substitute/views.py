from django.shortcuts import render, redirect, HttpResponse
from home import search
from .models import Substitute, Family
from home.models import Product, Rating
from home.forms import SearchForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def substitute(request, product_id, order=0):
    if request.method == "GET":
        substitutes = search.search_substitute(product_id, order)
        if substitutes.count() > 0:
            paginator = Paginator(substitutes, 6)
            page = request.GET.get("page")
            substitutes = paginator.get_page(page)
            context = {}
            context["substitutes"] = substitutes
            context["title"] = "Substituts"
            context["product"] = Product.objects.get(pk=product_id)
            context["form_search"] = SearchForm(None)
            context["order"] = order

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
                    context["note"] = Rating.objects.filter(
                        user_id=request.user, product_id=substitute
                    )
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
            return redirect(reverse("home:index"))


@csrf_exempt
def rating(request, product_id):
    product = Product.objects.get(pk=product_id)
    if product.average_rating is None:
        product.average_rating = 0
    tot_rating = Rating.objects.filter(product_id=product)

    return JsonResponse(
        {
            "whole_avg": int(round(product.average_rating)),
            "number_votes": tot_rating.count(),
            "dec_avg": round(product.average_rating, 1),
        }
    )


@csrf_exempt
def vote(request, product_id, actual_rating):
    product = Product.objects.get(pk=product_id)
    if request.method == "POST":
        try:
            nb_vote = 0
            ratings = 0
            tot_rating = Rating.objects.filter(product_id=product)
            for rating in tot_rating:
                nb_vote += 1
                ratings += rating.rating

            Rating.objects.create(
                rating=actual_rating, user_id=request.user, product_id=product
            )

            nb_vote += 1
            ratings += actual_rating
            product.average_rating = round(ratings / nb_vote, 1)
            product.save()
        except:
            pass

        if product.average_rating is None:
            product.average_rating = 0

        return JsonResponse(
            {
                "whole_avg": int(round(product.average_rating)),
                "number_votes": nb_vote,
                "dec_avg": round(product.average_rating, 1),
            }
        )
