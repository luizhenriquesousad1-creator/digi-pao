from decimal import Decimal

from django.conf import settings
from django.db import models
from catalog.models import Product


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Aguardando confirmação'
        CONFIRMED = 'CONFIRMED', 'Confirmado'
        PREPARING = 'PREPARING', 'Em preparação'
        READY = 'READY', 'Pronto para retirada'
        OUT_FOR_DELIVERY = 'OUT_FOR_DELIVERY', 'Saiu para entrega'
        COMPLETED = 'COMPLETED', 'Concluído'
        CANCELLED = 'CANCELLED', 'Cancelado'


    class FulfillmentMethod(models.TextChoices):
        PICKUP = 'PICKUP', 'Retirada na padaria'
        DELIVERY = 'DELIVERY', 'Entrega em domicílio'


    class PaymentMethod(models.TextChoices):
        CASH = 'CASH', 'Dinheiro'
        PIX = 'PIX', 'Pix'
        CARD = 'CARD', 'Cartão'


    customer = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT,
                             related_name='orders')

    status = models.CharField(max_length=20,
                          choices=Status.choices,
                          default=Status.PENDING)

    subtotal = models.DecimalField(max_digits=10,
                               decimal_places=2,
                               default=Decimal('0.00'))

    delivery_fee = models.DecimalField(max_digits=10,
                                   decimal_places=2,
                                   default=Decimal('0.00'))

    total = models.DecimalField(max_digits=10,
                            decimal_places=2,
                            default=Decimal('0.00'))

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    fulfillment_method = models.CharField(max_length=8,
                                      choices=FulfillmentMethod.choices)

    payment_method = models.CharField(max_length=4,
                                  choices=PaymentMethod.choices)

    delivery_address = models.TextField(blank=True,
                                    verbose_name='Endereço de entrega')

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-created_at']

    def __str__(self):
        return f"Pedido #{self.id} - {self.customer}"


class OrderItem(models.Model):

    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='items')

    product = models.ForeignKey(Product,
                                on_delete=models.PROTECT,
                                related_name='order_items')

    product_name = models.CharField(max_length=150,
                                    verbose_name='nome do produto')

    sale_unit = models.CharField(max_length=2,
                                 choices=Product.SaleUnit.choices,
                                 verbose_name='Unidade de venda')

    quantity = models.DecimalField(max_digits=10,
                                   decimal_places=3,
                                   verbose_name='quantidade')

    unit_price = models.DecimalField(max_digits=10,
                                     decimal_places=2,
                                     verbose_name='preço unitário')

    subtotal = models.DecimalField(max_digits=10,
                                   decimal_places=2,
                                   verbose_name='subtotal')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens dos pedidos'
        ordering = ['id']

    def __str__(self):
        return f"Pedido {self.product_name} - Pedido #{self.order.id}"
