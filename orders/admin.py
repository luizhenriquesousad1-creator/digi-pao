from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ('id',
                    'customer',
                    'status',
                    'fulfillment_method',
                    'payment_method',
                    'payment_method',
                    'total',
                    'created_at',
                    )

    list_filter = ('status',
                   'fulfillment_method',
                   'payment_method',
                   'created_at',
                   )

    search_fields = ('customer__username',
                     'customer__first_name',
                     'customer__last_name',
                     'customer__email',
                     )

    list_select_related = ('created_at',
                           'updated_at',
                           )

    ordering = ('-created_at',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = ('id',
                    'order',
                    'product_name',
                    'product',
                    'sale_unit',
                    'quantity',
                    'unit_price',
                    'subtotal',
                    'created_at',
                    )

    list_filter = ('sale_unit',
                   'created_at',
                   )

    search_fields = ('product_name',
                     'product__name',
                     )

    liste_select_related = ('order',
                            'product',
                            )

    readeonly_fields = ('created_at',)

    ordering = ('order', 'id',)
