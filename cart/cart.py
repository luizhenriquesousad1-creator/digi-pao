from decimal import Decimal
from catalog.models import Product
from django.core.exceptions import ValidationError


class Cart:

    def __init__(self, request):

        self.session = request.session

        self.cart = self.session.get('cart')

        if self.cart is None:

            self.cart = self.session['cart'] = {}

    def add(self, product, quantity=1):

        quantity = Decimal(str(quantity))

        if not product.is_active:
            raise ValidationError(
                'Este produto não está disponível para compra.'
            )

        if quantity <= 0:

            raise ValidationError('A quantidade deve ser maior que zero.')

        if product.sale_unit == Product.SaleUnit.UNIT:

            if quantity != quantity.to_integral_value():

                raise ValidationError('Produtos vendidos por unidade aceitam somente'
                                      ' quantidades inteiras.')

        elif product.sale_unit == Product.SaleUnit.KILOGRAM:

            if quantity % Decimal('0.100') != 0:

                raise ValidationError('Produtos vendidos por peso devem ser vendidos em unidades '
                                      'de 100 gramas.')

        product_id = str(product.id)

        current_quantity = Decimal(
            self.cart.get(product_id, {}).get('quantity', '0')
        )

        new_quantity = current_quantity + quantity

        if product.manage_stock:
            if new_quantity > product.stock_quantity:
                raise ValidationError(
                    'Quantidade solicitada superior ao estoque disponível.'
                )

        self.cart[product_id] = {
            'quantity': str(new_quantity)
        }

        self.session.modified = True

    def remove(self, product):

        product_id = str(product.id)

        if product_id in self.cart:

            del self.cart[product_id]

            self.session.modified = True

    def __iter__(self):

        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids, is_active=True)

        products_by_id = {str(product.id): product for product in products}

        for product_id, item in self.cart.copy().items():

            product = products_by_id.get(product_id)

            if product is None:
                del self.cart[product_id]
                self.session.modified = True
                continue

            quantity = Decimal(item['quantity'])

            price = product.price

            total_price = price * quantity

            yield {'product': product,
                   'quantity': quantity,
                   'price': price,
                   'total_price': total_price,
                   }

    def get_total_price(self):

        total = Decimal('0.00')

        for item in self:
            total += item['total_price']

        return total
