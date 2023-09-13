from django.contrib import admin

from elearning.warehouse.models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "product",
        "kind"
    )
    list_display_links = ("product",)
    list_filter = (
        "kind",
        "created",
        "modified"
    )
    fields = (
        "product",
        "text",
        "kind",
        "description",
        "created",
        "modified"
    )
    readonly_fields = (
        "created",
        "modified"
    )
    search_fields = (
        "product",
        "kind",
        "text"
    )
    search_help_text = "Can search by product, kind and text."
    ordering = ("product",)
    sortable_by = ("product", "kind")
    autocomplete_fields = ("product",)
    radio_fields = {"kind": admin.HORIZONTAL}
    save_on_top = True
    save_as = True
    date_hierarchy = "modified"
