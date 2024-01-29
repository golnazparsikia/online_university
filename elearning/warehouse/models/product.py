from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from painless.models.mixins import (
    TitleSlugMixin,
    StockUnitMixin,
    TimestampMixin,
    DescriptionMixin,
)
from elearning.warehouse.helper.consts import Scope, Difficulty


class Product(
    TitleSlugMixin,
    StockUnitMixin,
    TimestampMixin,
    DescriptionMixin
):
    """
    Represents a generic product in the system.
    Inherited from mixins to include common attributes.
    """
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        verbose_name=_("Parent Product"),
        related_name="children",
        null=True,
        blank=True,
        help_text=_("Refers to the main or higher-level item."),
    )

    scope = models.CharField(
        _("Product Group"),
        max_length=20,
        choices=Scope.choices,
        help_text=_(
            "Defines the category that this product group belongs to."
        ),
    )

    bundle = models.ManyToManyField("self", through="Bundle")

    is_buyable = models.BooleanField(
        _("Is Buyable"),
        default=False,
        help_text=_("Can users purchase this item?")
    )

    experience = models.FloatField(
        _("Experience"),
        default=0,
        help_text=_(
            "How users feel about using this item, often indicated by"
            "ratings or feedback."
        ),
    )

    difficulty = models.CharField(
        _("Difficulty"),
        max_length=20,
        null=True,
        choices=Difficulty.choices,
        help_text=_("Indicates the level of challenge or complexity."),
    )

    priority = models.PositiveIntegerField(
        _("Priority"),
        help_text=_(
            "Ranking items based on importance for resource"
            "allocation and decision-making."
        ),
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

        db_table_comment = (
            "All division, bootcamps, courses, projects, "
            "lessons, chapters and practices save in product table."
        )
        get_latest_by = ("created", "modified")

        default_manager_name = "objects"

        indexes = [
            models.Index(
                fields=("title",), name="title_idx"
            ),
            models.Index(fields=("parent",), name="parent_idx")
        ]

    constraints = [
        models.CheckConstraint(
            check=(Q(scope=Scope.DIVISION) | Q(parent=None)),
            name="division_valid_parent"
        ),
        models.CheckConstraint(
            check=(Q(scope=Scope.BOOTCAMP) | Q(parent__scope=Scope.DIVISION)),
            name="Bootcamp_valid_parent"
        ),
        models.CheckConstraint(
            check=(Q(scope=Scope.PROJECT) | Q(parent__scope=Scope.BOOTCAMP)),
            name="project_valid_parent"
        ),
        models.CheckConstraint(
            check=(Q(scope=Scope.COURSE) | Q(parent=None)),
            name="course_valid_parent"
        ),
        models.CheckConstraint(
            check=(Q(scope=Scope.LESSON) | Q(parent__scope=Scope.COURSE)),
            name="lesson_valid_parent"
        ),
        models.CheckConstraint(
            check=(Q(scope=Scope.CHAPTER) | Q(parent__scope=Scope.LESSON)),
            name="chapter_valid_parent"
        ),
        models.CheckConstraint(
            check=(Q(scope=Scope.PRACTICE) | Q(parent__scope=Scope.CHAPTER)),
            name="practice_valid_parent"
        ),
        models.CheckConstraint(
            check=Q(scope__in=Scope.values),
            name="product_valid_scope"
        ),
        models.CheckConstraint(
            check=(Q(is_buyable=False) | ~Q(scope=Scope.COURSE)),
            name="not_buyable_for_no_course_products"
        )
    ]

    def clean(self):
        if self.scope == Scope.DIVISION and self.parent is not None:
            raise ValidationError(
                {"parent": _("Invalid parent for the division.")}
            )
        if self.scope == Scope.BOOTCAMP and self.parent.scope != Scope.DIVISION:
            raise ValidationError(  
                {"parent": _("Invalid parent for the bootcamp.")}
            )
        if self.scope == Scope.COURSE and self.parent is not None:
            raise ValidationError(
                {"parent": _("Invalid parent for the course.")}
            )
        if self.scope == Scope.PROJECT and self.parent.scope != Scope.BOOTCAMP:
            raise ValidationError(
                {"parent": _("Invalid parent for the project.")}
            )
        if self.scope == Scope.LESSON and self.parent.scope != Scope.COURSE:
            raise ValidationError(
                {"parent": _("Invalid parent for the lesson.")}
            )
        if self.scope == Scope.CHAPTER and self.parent.scope != Scope.LESSON:
            raise ValidationError(
                {"parent": _("Invalid parent for the chapter.")}
            )
        if self.scope == Scope.PRACTICE and self.parent.scope != Scope.LESSON:
            raise ValidationError(
                {"parent": _("Invalid parent for the practice.")}
            )
        if self.scope != Scope.COURSE and self.is_buyable == True:
            raise ValidationError(
                {"is_buyable": _("All the products except courses are not buyable.")}
            )

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

class Division(Product):
    """Proxy model representing a division."""
    class Meta:
        proxy = True,
        verbose_name = _("Division"),
        verbose_name_plural = _("Divisions")

class Bootcamp(Product):
    """Proxy model representing a bootcamp."""
    class Meta:
        proxy = True,
        verbose_name = _("Bootcamp"),
        verbose_name_plural = _("Bootcamps")

class Course(Product):
    """Proxy model representing a Course."""
    class Meta:
        proxy = True,
        verbose_name = _("Course"),
        verbose_name_plural = _("Courses")

class Lesson(Product):
    """Proxy model representing a lesson."""
    class Meta:
        proxy = True,
        verbose_name = _("Lesson"),
        verbose_name_plural = _("Lessons")

class Chapter(Product):
    """Proxy model representing a Chapter."""
    class Meta:
        proxy = True,
        verbose_name = _("Chapter"),
        verbose_name_plural = _("Chapters")

class Project(Product):
    """Proxy model representing a Project."""
    class Meta:
        proxy = True,
        verbose_name = _("Project"),
        verbose_name_plural = _("Projects")

class Practice(Product):
    """Proxy model representing a Practice."""
    class Meta:
        proxy = True,
        verbose_name = _("Practice"),
        verbose_name_plural = _("Practices")
