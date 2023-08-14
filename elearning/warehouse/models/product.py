from django.db import models
from django.utils.translation import gettext_lazy as _

from painless.models.mixins import (
    TitleSlugMixin,
    StockUnitMixin,
    TimestampMixin,
    DescriptionMixin,
)
from elearning.warehouse.helper.consts import SCOPE, DIFFICULTY


class Product(TitleSlugMixin, StockUnitMixin, TimestampMixin, DescriptionMixin):      # noqa: E501
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
        choices=SCOPE.choices,
        help_text=_("Defines the category that this product group belongs to."),   # noqa: E501
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
        choices=DIFFICULTY.choices,
        help_text=_("Indicates the level of challenge or complexity."),
    )

    priority = models.PositiveIntegerField(
        _("Priority"),
        help_text=_(
            "Ranking items based on importance for resource"
            "allocation and decision-making."
        ),
    )

    class Meta:
        db_table_comment = (
            "All division, bootcamps, courses, projects, "
            "lessons, chapters and practices save in product table."
        )
        get_latest_by = ("created", "modified")

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.scope}({self.title})"
