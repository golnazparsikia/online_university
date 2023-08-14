from django.contrib import admin

from elearning.warehouse.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_buyable",
        "difficulty",
        "created",
        "modified"
    )
    list_display_links = ("title",)
    list_editable = ("is_buyable", "difficulty")

    list_filter = (
        "difficulty",
        "is_buyable",
        "created",
        "modified"
    )

    fieldsets = [
        (
            "Basic Information",
            {
                "fields": ("title", "slug", "sku", "description"),
                "description": "Essential product details like name, link, "
                "code, and description."
            }
        ),
        (
            "Product Hierarchy",
            {
                "fields": ("parent",),
                "classes": ("collapse",),
                "description": "Connect related products by setting a parent "
                "item."
            },
        ),
        (
            "Product Details",
            {
                "fields": ("scope", "is_buyable", "difficulty", "priority", "experience"),    # noqa: E501
                "classes": ("collapse",),
                "description": "Define type, availability, and visibility of "
                "the product."
            },
        ),
        (
            "Security",
            {
                "fields": ("created", "modified"),
                "classes": ("collapse",),
                "description": "Record the time when an item is created or "
                "modified."
            },
        )
    ]

    readonly_fields = (
        "slug",
        "sku",
        "experience",
        "created",
        "modified"
    )

    search_fields = (
        "title",
        "scope",
        "difficulty"
    )
    search_help_text = "Can search by title, scope and difficulty."

    ordering = ("title",)
    sortable_by = ("title", "created", "modified")

    autocomplete_fields = ("parent",)
    radio_fields = {"scope": admin.HORIZONTAL}

    list_per_page = 50

    save_on_top = True
    save_as = True

    date_hierarchy = "modified"
