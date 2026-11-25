from decimal import Decimal
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from catalog.models import Category, Product
from cart.cart import Cart
from django.core.exceptions import ValidationError


class CartTests(TestCase):

    def setUp(self):

        self.factory = RequestFactory()

        self.request = self.factory.get('/')

        middleware = SessionMiddleware(lambda request: None)

        middleware.process_request(self.request)

        self.cart = Cart(self.request)

        self.category = Category.objects.create(name='Categoria de teste')

        self.unit_product = Product.objects.create(name='Pão Francês',
                                                   category=self.category,
                                                   sale_unit=Product.SaleUnit.UNIT,
                                                   price=Decimal('0.50'),
                                                   stock_quantity=Decimal('100.000'),
                                                   manage_stock=True,
                                                   )

        self.weight_product = Product.objects.create(name='Pão de Queijo',
                                                     category=self.category,
                                                     sale_unit=Product.SaleUnit.KILOGRAM,
                                                     price=Decimal('16.00'),
                                                     stock_quantity=Decimal('5.000'),
                                                     manage_stock=True,
                                                    )

    def test_add_product(self):

        self.cart.add(self.unit_product, quantity=2)

        product_id = str(self.unit_product.id)

        self.assertEqual(self.cart.cart[product_id]['quantity'], '2')

    def test_add_same_product(self):

        self.cart.add(self.unit_product, quantity=2)

        self.cart.add(self.unit_product, quantity=3)

        product_id = str(self.unit_product.id)

        self.assertEqual(self.cart.cart[product_id]['quantity'], '5')

    def test_add_weight_product(self):

        self.cart.add(self.weight_product, quantity=Decimal('0.300'))

        product_id = str(self.weight_product.id)

        self.assertEqual(self.cart.cart[product_id]['quantity'], '0.300')

    def test_reject_invalid_weight_quantity(self):

        with self.assertRaises(ValidationError):

            self.cart.add(self.weight_product, quantity=Decimal('0.350'))

        product_id = str(self.weight_product.id)

        self.assertNotIn(product_id, self.cart.cart)

    def test_reject_quantity_above_stock(self):

        with self.assertRaises(ValidationError):

            self.cart.add(self.unit_product, quantity=101)

        product_id = str(self.unit_product.id)

        self.assertNotIn(product_id, self.cart.cart)

    def test_add_quantity_equal_to_stock(self):

        self.cart.add(self.unit_product, quantity=100)

        product_id = str(self.unit_product.id)

        self.assertEqual(self.cart.cart[product_id]['quantity'], '100')

    def test_reject_fractional_unit_quantity(self):

        with self.assertRaises(ValidationError):

            self.cart.add(self.unit_product, quantity=Decimal('1.5'))

        product_id = str(self.unit_product.id)

        self.assertNotIn(product_id, self.cart.cart)

    def test_reject_accumulated_quantity_above_stock(self):

        self.cart.add(self.unit_product, quantity=80)

        with self.assertRaises(ValidationError):

            self.cart.add(self.unit_product, quantity=30)

        product_id = str(self.unit_product.id)

        self.assertEqual(self.cart.cart[product_id]['quantity'], '80')

    def test_reject_inactive_product(self):

        self.unit_product.is_active = False

        self.unit_product.save()

        with self.assertRaises(ValidationError):

            self.cart.add(self.unit_product, quantity=1)

        product_id = str(self.unit_product.id)

        self.assertNotIn(product_id, self.cart.cart)

    def test_remove_product(self):

        self.cart.add(self.unit_product, quantity=1)

        product_id = str(self.unit_product.id)

        self.cart.remove(self.unit_product)

        self.assertNotIn(product_id, self.cart.cart)
