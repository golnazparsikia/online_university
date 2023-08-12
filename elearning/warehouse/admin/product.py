from django.contrib import admin

from elearning.warehouse.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 
                    'difficulty',
                    'is_buyable',
                    'modified',
                    'created'
                    )
    list_filter = (
        'is_buyable',
        'modified',
        'created'
    )
    search_fields = (
        'title',
    )
    readonly_fields = (
        'modified',
        'created',
        'sku',
        'slug'
    )
    save_on_top = True
    save_as = True 
