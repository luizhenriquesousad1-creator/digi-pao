from decimal import InvalidOperation
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from catalog.models import Product
from .cart import Cart


@require_POST
def add_to_cart(request, product_id):

    product = get_object_or_404(Product, pk=product_id)

    quantity = request.POST.get('quantity', '1')

    cart = Cart(request)

    try: cart.add(product, quantity=quantity)

    except ValidationError as error:
        messages.error(request, error.messages[0])

    except (InvalidOperation, ValueError):
        messages.error(request, 'Informe uma quantidade válida.')

    else:
        messages.success(request,
                           f'{product.name} foi adicionado ao carrinho.')

    return redirect('catalog:product_list')

def cart_detail(request):

    cart = Cart(request)

    total = cart.get_total_price()

    context = {'cart': cart,
               'total': total,}

    return render(request, 'cart/cart_detail.html', context)

@require_POST
def remove_from_cart(request, product_id):

    product = get_object_or_404(Product, pk=product_id)

    cart = Cart(request)
    cart.remove(product)

    messages.success(
        request,
        f'{product.name} foi removido do carrinho.'
    )

    return redirect('cart:cart_detail')