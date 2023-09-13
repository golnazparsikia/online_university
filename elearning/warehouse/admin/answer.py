from django.contrib import admin
from django.db.models import QuerySet

from elearning.warehouse.models import (
    Answer,
    Checkbox,
    Radio,
    Placeholder,
    Conditional,
    Code
)

from elearning.warehouse.helper.consts import QuestionType

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
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

@admin.register(Checkbox)
class CheckboxAdmin(AnswerAdmin):
    """
    Admin configuration for the Checkbox model.
    """
    def get_queryset(self, request, *args,  **kwargs) -> QuerySet[Checkbox]:
        qs = super().get_queryset(request, *args,  **kwargs)
        qs = qs.filter(question__kind=QuestionType.CHECKBOX)
        return qs

@admin.register(Radio)
class RadioAdmin(AnswerAdmin):
    """
    Admin configuration for the Radio model.
    """
    def get_queryset(self, request, *args,  **kwargs) -> QuerySet[Radio]:
        qs = super().get_queryset(request, *args,  **kwargs)
        qs = qs.filter(question__kind=QuestionType.RADIO)
        return qs

@admin.register(Placeholder)
class PlaceholderAdmin(AnswerAdmin):
    """
    Admin configuration for the Placeholder model.
    """
    def get_queryset(self, request, *args,  **kwargs) -> QuerySet[Placeholder]:
        qs = super().get_queryset(request, *args,  **kwargs)
        qs = qs.filter(question__kind=QuestionType.PLACEHOLDER)
        return qs

@admin.register(Conditional)
class ConditionalAdmin(AnswerAdmin):
    """
    Admin configuration for the Conditional model.
    """
    def get_queryset(self, request, *args,  **kwargs) -> QuerySet[Conditional]:
        qs = super().get_queryset(request, *args,  **kwargs)
        qs = qs.filter(question__kind=QuestionType.CONDITIONAL)
        return qs

@admin.register(Code)
class CodeAdmin(AnswerAdmin):
    """
    Admin configuration for the Code model.
    """
    def get_queryset(self, request, *args,  **kwargs) -> QuerySet[Code]:
        qs = super().get_queryset(request, *args,  **kwargs)
        qs = qs.filter(question__kind=QuestionType.CODE)
        return qs
