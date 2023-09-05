from django.contrib import admin
from shop.basket.models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'slug', 
        'user', 
        'product',
    )

    list_filter = (
        'user', 
        'product',
    )

    search_fields = (
        'slug', 
        'user__username', 
        'product__name'
        )
    
    readonly_fields = (
        'id',
    ) 

    fieldsets = (
        (("General Information"),
        {
            'fields': ('id', 'slug', 'user', 'product', 'created_at'),
        }
        ),
        (("Additional Information"),
        {
            'fields': ('some_other_field',),
        }
        ),
    )