from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from decimal import Decimal


class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='nome'
    )

    description = models.TextField(
        blank=True,
        verbose_name='descrição'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='categoria ativa'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):

    class SaleUnit(models.TextChoices):
        UNIT = 'UN', 'Unidade'
        KILOGRAM = 'KG', 'Quilograma'

    name = models.CharField(
        max_length=150,
        verbose_name='nome'
    )

    description = models.TextField(
        blank=True,
        verbose_name=  'descrição'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='categoria'
    )

    sale_unit = models.CharField(
        max_length=2,
        choices=SaleUnit.choices,
        default=SaleUnit.UNIT,
        verbose_name='unidade de venda'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='preço'
    )

    stock_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        default=Decimal('0.000'),
        validators=[MinValueValidator(Decimal('0.000'))],
        verbose_name='quantidade em estoque'
    )

    manage_stock = models.BooleanField(
        default=True,
        verbose_name='controlar estoque'
    )

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name='fotografia'
    )

    is_active= models.BooleanField(
        default=True,
        verbose_name='produto ativo'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def clean(self):
        super().clean()

        if (self.manage_stock and
            self.sale_unit == self.SaleUnit.UNIT
            and self.stock_quantity is not None
            and self.stock_quantity != self.stock_quantity.to_integral_value()):
            raise ValidationError(
            {'stock_quantity': 'Produtos vendidos por unidade devem ter estoque inteiro.'
            })


    class Meta:
        verbose_name = 'produto'
        verbose_name_plural = 'produtos'
        ordering = ["name"]

    def __str__(self):
        return self.name