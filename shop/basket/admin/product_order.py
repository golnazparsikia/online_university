from django.contrib import admin
from shop.basket.models import ProductOrder

@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):


    list_display = (
        'cost',
        'is_refunded',
        'order',
        'product',
        'modified',
        'created',
    )


    list_filter = (
        'is_refunded',
    )


    search_fields = (
        'order__transaction_number',
        'product__name',
    )


    readonly_fields = (
        'id',
        'cost',
        'created',
        'modified',
    )


    autocomplete_fields = (
        'order',    
        'product',  
    )


    fieldsets = (
        (("Product Order Information"), {
            'fields': (
                'id',
                'cost',
                'is_refunded',
            )
        }),
        (("Related Objects"), {
            'fields': (
                'order',
                'product',
            )
        }),
        (("Security"), {
            'fields': (
                "created",
                "modified",
            ),
            'classes': ('collapse',),
        }),
    )
