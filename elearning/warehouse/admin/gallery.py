from django.contrib import admin
from elearning.warehouse.models import Gallery

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Gallery model.

    This class provides a customized admin interface for managing Gallery instances.

    Attributes:
        list_display (tuple): A tuple containing fields to be displayed in the list view of the admin page.
        search_fields (tuple): A tuple containing fields to enable search functionality in the admin page.
        search_help_text (str): Help text displayed for search functionality.
        readonly_fields (tuple): A tuple containing fields that are read-only in the admin page.
        save_on_top (bool): Whether to show the save buttons at the top of the admin page.
        fieldsets (tuple): A tuple of tuples defining the structure of form fields in the admin page.
    """

    list_display = ("title",)
    search_fields = ("title", )
    search_help_text = "You can search by title"
    readonly_fields = (
        "modified",
        "created"
    )
    save_on_top = True

    fieldsets = (
        ("basic information", {
            "fields": (
                "title",
                "picture",
                "alternate_text",
            ),
        }),
        ("security", {
            "fields": (
                "modified",
                "created",
            ),
            "classes": (
                "collapse",
            ),
        }),
    )


