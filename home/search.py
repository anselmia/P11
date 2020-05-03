from home.models import Product


def search_product(text, order):
    queryset = Product.objects.filter(name__icontains=text,)
    if order == 0:
        queryset = queryset.order_by("name")
    elif order == 1:
        queryset = queryset.order_by("nutriscore")
    else:
        queryset = queryset.order_by("-average_rating")
    return queryset


def search_substitute(id, order):
    product = Product.objects.get(pk=id)
    category = product.category_id
    queryset = Product.objects.filter(category_id_id=category.id).exclude(id=id)
    if order == 0:
        queryset = queryset.order_by("nutriscore")
    elif order == 1:
        queryset = queryset.order_by("name")
    else:
        queryset = queryset.order_by("-average_rating")
    return queryset
