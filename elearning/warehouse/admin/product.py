from django.contrib import admin
from django.db.models import QuerySet

from elearning.warehouse.models import (
    Product,
    Division,
    Bootcamp,
    Course,
    Lesson,
    Chapter,
    Project,
    Practice
)
from elearning.warehouse.forms.product import (
    DivisionForm,
    BootcampForm,
    CourseForm,
    LessonForm,
    ChapterForm,
    ProjectForm,
    PracticeForm
)

from elearning.warehouse.helper.consts import Scope


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Product model.
    """
    list_display = (
        "title",
        "scope",
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

@admin.register(Division)
class DivisionAdmin(ProductAdmin):
    """
    Admin configuration for the Division model.
    """
    form = DivisionForm
    def get_queryset(self, request, *args,  **kwargs) -> QuerySet[Division]:
        qs = super().get_queryset(request, *args,  **kwargs)
        qs = qs.filter(scope=Scope.DIVISION)
        return qs

@admin.register(Bootcamp)
class BootcampAdmin(ProductAdmin):
    """
    Admin configuration for the Bootcamp model.
    """
    form = BootcampForm
    def get_queryset(self, request, *args,  **kwargs) -> QuerySet[Bootcamp]:
        qs = super().get_queryset(request, *args,  **kwargs)
        qs = qs.filter(scope=Scope.BOOTCAMP)
        return qs

@admin.register(Course)
class CourseAdmin(ProductAdmin):
    """
    Admin configuration for the Course model.
    """
    form = CourseForm
    def get_queryset(self, request, *args,  **kwargs) -> QuerySet[Course]:
        qs = super().get_queryset(request, *args,  **kwargs)
        qs = qs.filter(scope=Scope.COURSE)
        return qs

@admin.register(Lesson)
class LessonAdmin(ProductAdmin):
    """
    Admin configuration for the Lesson model.
    """
    form = LessonForm
    def get_queryset(self, request, *args,  **kwargs) -> QuerySet[Lesson]:
        qs = super().get_queryset(request, *args,  **kwargs)
        qs = qs.filter(scope=Scope.LESSON)
        return qs

@admin.register(Chapter)
class ChapterAdmin(ProductAdmin):
    """
    Admin configuration for the Chapter model.
    """
    form = ChapterForm
    def get_queryset(self, request, *args,  **kwargs) -> QuerySet[Chapter]:
        qs = super().get_queryset(request, *args,  **kwargs)
        qs = qs.filter(scope=Scope.CHAPTER)
        return qs

@admin.register(Project)
class ProjectAdmin(ProductAdmin):
    """
    Admin configuration for the Project model.
    """
    form = ProjectForm
    def get_queryset(self, request, *args,  **kwargs) -> QuerySet[Project]:
        qs = super().get_queryset(request, *args,  **kwargs)
        qs = qs.filter(scope=Scope.PROJECT)
        return qs

@admin.register(Practice)
class PracticeAdmin(ProductAdmin):
    """
    Admin configuration for the Practice model.
    """
    form = PracticeForm
    def get_queryset(self, request, *args,  **kwargs) -> QuerySet[Practice]:
        qs = super().get_queryset(request, *args,  **kwargs)
        qs = qs.filter(scope=Scope.PRACTICE)
        return qs
