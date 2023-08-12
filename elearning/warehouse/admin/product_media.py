from django.contrib import admin
from django.utils.text import slugify
from elearning.warehouse.models import ProductMedia

@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'duration', 
        'modified',
        'created'
        )
    list_filter = (
        'duration',
        'modified',
        'created'
    )
    search_fields = (
        'duration',
        'product'
    )
    readonly_fields = (
        'modified',
        'created',
        'sku',
        'slug'
    )
    save_on_top = True
    save_as = True
    autocomplete_fields = (
        'product',
        ) 