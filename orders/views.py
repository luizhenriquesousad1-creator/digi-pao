from decimal import Decimal, ROUND_HALF_UP

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect

from cart.cart import Cart
from catalog.models import Product
from .forms import CheckoutForm
from .models import Order, OrderItem


@login_required
def checkout(request):

    cart = Cart(request)
    cart_items = list(cart)

    if not cart_items:
        messages.warning(request, 'Seu carrinho está vazio.')
        return redirect('cart:cart_detail')

    cent = Decimal('0.01')

    subtotal_preview = sum(
        (
            (item['price'] * item['quantity']).quantize(
                cent, rounding=ROUND_HALF_UP
            )
            for item in cart_items
        ),
        Decimal('0.00')
    )

    if request.method == 'POST':

        form = CheckoutForm(request.POST)

        if form.is_valid():

            try:
                with transaction.atomic():

                    product_ids = [
                        item['product'].id for item in cart_items
                    ]

                    locked_products = Product.objects.select_for_update().filter(
                        id__in=product_ids,
                        is_active=True
                    )

                    products_by_id = {
                        product.id: product
                        for product in locked_products
                    }

                    if len(products_by_id) != len(set(product_ids)):
                        raise ValidationError(
                            'Um ou mais produtos não estão mais disponíveis.'
                        )

                    prepared_items = []
                    subtotal = Decimal('0.00')

                    for item in cart_items:

                        product = products_by_id[item['product'].id]
                        quantity = item['quantity']

                        if quantity <= 0:
                            raise ValidationError(
                                'Existe uma quantidade inválida no carrinho.'
                            )

                        if product.sale_unit == Product.SaleUnit.UNIT:
                            if quantity != quantity.to_integral_value():
                                raise ValidationError(
                                    'Produtos vendidos por unidade '
                                    'exigem quantidades inteiras.'
                                )

                        elif product.sale_unit == Product.SaleUnit.KILOGRAM:
                            if quantity % Decimal('0.100') != 0:
                                raise ValidationError(
                                    'Produtos vendidos por peso '
                                    'devem respeitar incrementos de 100 gramas.'
                                )

                        if product.manage_stock:
                            if quantity > product.stock_quantity:
                                raise ValidationError(
                                    f'Estoque insuficiente para {product.name}.'
                                )

                        line_subtotal = (
                            product.price * quantity
                        ).quantize(cent, rounding=ROUND_HALF_UP)

                        subtotal += line_subtotal

                        prepared_items.append({
                            'product': product,
                            'quantity': quantity,
                            'unit_price': product.price,
                            'subtotal': line_subtotal,
                        })

                    delivery_fee = Decimal('0.00')
                    total = subtotal + delivery_fee

                    order = Order.objects.create(
                        customer=request.user,
                        fulfillment_method=form.cleaned_data[
                            'fulfillment_method'
                        ],
                        payment_method=form.cleaned_data['payment_method'],
                        delivery_address=form.cleaned_data['delivery_address'],
                        subtotal=subtotal,
                        delivery_fee=delivery_fee,
                        total=total,
                    )

                    for item in prepared_items:

                        product = item['product']

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            product_name=product.name,
                            sale_unit=product.sale_unit,
                            quantity=item['quantity'],
                            unit_price=item['unit_price'],
                            subtotal=item['subtotal'],
                        )

                        if product.manage_stock:
                            product.stock_quantity -= item['quantity']
                            product.save(
                                update_fields=['stock_quantity', 'updated_at']
                            )

            except ValidationError as error:
                messages.error(request, error.messages[0])
                return redirect('cart:cart_detail')

            # Limpar o carrinho após a conclusão da transação
            request.session['cart'] = {}
            request.session.modified = True

            messages.success(
                request,
                f'Pedido #{order.id} realizado com sucesso!'
            )

            return redirect('catalog:product_list')

    else:
        form = CheckoutForm()

    context = {
        'form': form,
        'cart_items': cart_items,
        'subtotal': subtotal_preview,
        'total': subtotal_preview,
    }

    return render(request, 'orders/checkout.html', context)