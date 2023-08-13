from django.db import models
from django.utils.translation import gettext_lazy as _

from painless.models.mixins.common import TimestampMixin


class Bundle(TimestampMixin):
    bootcamp = models.ForeignKey(
        "Product",
        on_delete=models.PROTECT,
        verbose_name=_("Bootcamp"),
        related_name="bootcamps",
        null=True,
        help_text=_("For the learning program or workshop.")
    )

    course = models.ForeignKey(
        "Product",
        on_delete=models.PROTECT,
        verbose_name=_("Course"),
        related_name="courses",
        null=True,
        help_text=_("Pertaining to a specific subject of study.")
    )

    def __str__(self):
        return f"({self.bootcamp}, {self.course})"

    def __repr__(self):
        return f"{self.__class__.__name__}: ({self.bootcamp}, {self.course})"
