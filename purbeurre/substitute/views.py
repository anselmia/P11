from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from home import search
from .models import Substitute
from home.models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def substitute(request, **kwarg):
    if request.method == 'GET':
        id_product = kwarg['product_id']
        substitutes = search.search_substitute(id_product)
        if substitutes.count() > 0:
            paginator = Paginator(substitutes, 6)
            page = request.GET.get('page')
            substitutes = paginator.get_page(page)
            context = {}
            context['substitutes'] = substitutes
            context['title'] = 'Substitute'
            context['product'] = Product.objects.get(pk=id_product)
            
            return render(request, 'substitute.html', context)
        else:   
            context = {'message': 'noresults'}
            return render(request, 'home.html', context)

def detail(request, product_id, substitute_id):
    if request.method == 'GET':
        #id_substitute = kwarg['substitute_id']
        substitute = Product.objects.get(pk=substitute_id)
        #id_product = kwarg['product_id']
        product = Product.objects.get(pk=product_id)
        if substitute is not None:
            context = {}
            context['product'] = product
            context['substitute'] = substitute
            context['title'] = 'Détails du produit ' + substitute.name 
            if request.user.is_authenticated:
                context['exist'] = Substitute.objects.filter(user_id=request.user, product_id=product, substitute_id=substitute).exists()
            
            return render(request, 'detail.html', context)
        else:   
            context = {'message': 'noresults'}
            return render(request, 'home.html', context)

@login_required
def save(request, product_id, substitute_id):
    if request.method == 'GET' and product_id and substitute_id:        
        substitute = Product.objects.get(pk=substitute_id)
        product = Product.objects.get(pk=product_id)   
        context = {} 
        context['product'] = product
        context['substitute'] = substitute
        context['title'] = 'Détails du produit ' + substitute.name     
        if Substitute.objects.filter(user_id=request.user, product_id=product, substitute_id=substitute).exists():
            messages.warning(request, 'Vous avez déjà enregistré ce substitut')
        else:    
            try:
                user_product = Substitute(user_id=request.user, product_id=product, substitute_id=substitute)
                user_product.save()
                messages.success(request, 'Votre substitut a été sauvé')
                
            except:
                pass
        
        return render(request, 'detail.html', context)

@login_required
def detail_favoris(request, product_id, substitute_id):
    if request.method == 'GET':
        substitute = Product.objects.get(pk=substitute_id)
        product = Product.objects.get(pk=product_id)
        if substitute is not None and product is not None:
            context = {}
            context['product'] = product
            context['substitute'] = substitute
            context['title'] = 'Détails du favoris'
            
            return render(request, 'detail_favoris.html', context)
        else:   
            context = {'message': 'noresults'}
            return render(request, 'favorites.html', context)