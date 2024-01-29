from django.contrib import admin

from elearning.warehouse.models import QuestionHelp


@admin.register(QuestionHelp)
class QuestionHelpAdmin(admin.ModelAdmin):
    list_display = (
        "question",
        "plain_text",
        "created",
        "modified"
    )
    list_display_links = ("question",)

    list_filter = (
        "created",
        "modified"
    )

    fieldsets = (
        (
            "Question Reference",
            {
                "fields": ("question",),
                "description": "Connect this help to a specific question for "
                "better understanding."
            }
        ),
        (
            "Text and HTML help",
            {
                "fields": ("plain_text", "picture", "html_code", "code"),
                "description": "Provide explanations using plain text or "
                "formatted HTML, along with a specified code style.",
                "classes": "collapse"
            }
        ),
        (
            "Visual Help",
            {
                "fields": ("alternate_text", "width_field", "height_field"),
                "description": "Image and Enhance understanding with images."
            }
        )
    )

    readonly_fields = (
        "created",
        "modified"
    )

    search_fields = (
        "question",
        "plain_text",
        "alternate_text"
    )
    search_help_text = "Can search by question, plain_text, alternate_text."

    ordering = ("question",)
    sortable_by = ("question", "created", "modified")

    autocomplete_fields = ("question",)

    list_per_page = 50

    save_on_top = True
    save_as = True

    date_hierarchy = "modified"
