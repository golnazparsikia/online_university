from django.contrib import admin

from elearning.warehouse.models import Bundle


@admin.register(Bundle)
class BundleAdmin(admin.ModelAdmin):
    list_display = (
        "bootcamp",
        "course",
        "created",
        "modified"
    )
    list_display_links = (
        "bootcamp",
        "course"
    )

    list_filter = (
        "created",
        "modified"
    )

    fields = (
        "bootcamp",
        "course",
        "created",
        "modified"
    )

    readonly_fields = (
        "created",
        "modified"
    )

    ordering = ("bootcamp",)
    sortable_by = (
        "bootcamp",
        "course",
        "created",
        "modified"
    )

    search_fields = (
        "bootcamp",
        "course"
    )
    search_help_text = "Can search by bootcamp and course."

    autocomplete_fields = ("bootcamp", "course")

    list_per_page = 50

    save_on_top = True
    save_as = True

    date_hierarchy = "modified"
