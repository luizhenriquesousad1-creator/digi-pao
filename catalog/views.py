from django.shortcuts import render
from catalog.models import Product


def product_list(request):

    products = Product.objects.filter(is_active=True)

    context = {'products': products}

    return render(request, 'catalog/product_list.html', context)