from django.contrib import admin

from elearning.warehouse.models import Answer


@admin.register(Answer)
class Answer(admin.ModelAdmin):
    list_display = (
        "question",
        "is_correct",
        "priority",
        "created",
        "modified"
    )
    list_display_links = ("question", "priority")
    list_editable = ("is_correct",)

    list_filter = (
        "created",
        "modified"
    )

    readonly_fields = (
        "created",
        "modified"
    )

    search_fields = (
        "question",
        "priority"
    )
    search_help_text = "Can search by question and priority."

    ordering = ("question",)

    autocomplete_fields = ("question",)

    list_per_page = 50

    save_on_top = True
    save_as = True

    date_hierarchy = "modified"
