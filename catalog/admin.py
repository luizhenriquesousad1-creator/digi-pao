from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class Categoryadmin(admin.ModelAdmin):
    list_display =(
        'name',
        'is_active',
        'created_at',
        'updated_at'
    )

    list_filter = ('is_active',)

    search_fields = ('name', 'description')

    ordering = ('name',)

    readonly_fields = ('created_at', 'updated_at')

@admin.register(Product)
class Productadmin(admin.ModelAdmin):
    lista_display = (
        'name',
        'category',
        'sale_price',
        'price',
        'stock_quantity',
        'manage_stock',
        'is_active',
    )


    list_filter = (
        'category',
        'sale_unit',
        'manage_stock',
        'is_active',
    )


    search_fields = (
        'name',
        'description',
        'category__name',)


    list_select_related = ('category',)

    ordering = ('name',)


    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Informações do produto', {
            'fields': (
                'name',
                'description',
                'category',
                'image',
            ),
        }),

        ('Comercialização', {
            'fields': (
                'sale_unit',
                'price',
            ),
        }),

        ('Estoque', {
            'fields': (
                'manage_stock',
                'stock_quantity',
            ),
        }),

        ('Disponibilidade', {
            'fields': ('is_active',),
        }),

        ('Datas', {
            'fields': (
                'created_at',
                'updated_at',
            ),
        }),
    )
