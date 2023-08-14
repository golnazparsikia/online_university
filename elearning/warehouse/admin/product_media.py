from django.contrib import admin

from elearning.warehouse.models import ProductMedia


@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "created",
        "modified"
    )
    list_display_links = ("product",)

    list_filter = (
        "product",
        "duration"
    )

    fieldsets = (
        (
            "Product Information",
            {
                "fields": ("product", "sku"),
                "description": "Connect this media to a specific product."
            },
        ),
        (
            "Media Information",
            {
                "fields": ("alternate_text", "width_field", "height_field", "duration"),   # noqa: #501
                "classes": ("collapse",),
                "description": "Provide extra information about the visuals."
            }
        ),
        (
            "Security",
            {
                "fields": ("created", "modified"),
                "classes": ("collapse",),
                "description": "Record the time when an item is created or"
                "modified."
            }
        )
    )

    readonly_fields = (
        "sku",
        "created",
        "modified"
    )

    search_fields = ("product",)
    search_help_text = "Can search by product."

    ordering = ("product",)
    sortable_by = ("product", "created", "modified")

    autocomplete_fields = ("product",)

    list_per_page = 50

    save_on_top = True
    save_as = True

    date_hierarchy = "modified"
