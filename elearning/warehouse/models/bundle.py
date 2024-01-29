from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from painless.models.mixins import TimestampMixin
from ..helper.consts import Scope


class Bundle(TimestampMixin):
    bootcamp = models.ForeignKey(
        "Product",
        on_delete=models.PROTECT,
        verbose_name=_("Bootcamp"),
        related_name="bootcamps",
        null=True,
        limit_choices_to={"scope": Scope.BOOTCAMP},
        help_text=_("For the learning program or workshop."),
    )

    course = models.ForeignKey(
        "Product",
        on_delete=models.PROTECT,
        verbose_name=_("Course"),
        related_name="courses",
        null=True,
        limit_choices_to={"scope": Scope.COURSE},
        help_text=_("Pertaining to a specific subject of study."),
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _("Bundle")
        verbose_name_plural = _("Bundles")

        db_table_comment = (
            "Intermediate model to connect with product model."
        )
        get_latest_by = ("created", "modified")

        default_manager_name = "objects"

        constraints = [
            models.UniqueConstraint(
                fields=["bootcamp", "course"],
                name="bootcamp_course_uniqueness"
            )
        ]

    def clean(self):
        if self.bootcamp.scope != Scope.BOOTCAMP:
            raise ValidationError(
                {"bootcamp": "Invalid product."}
            )
        if self.course.scope != Scope.COURSE:
            raise ValidationError(
                {"course": "Invalid product."}
            )

        is_duplicate = self.__class__.objects.exclude(pk=self.pk).filter(
            bootcamp=self.bootcamp, course=self.course).exists()
        if is_duplicate:
            raise ValidationError(_("Duplicated bootcamp and course."))

    def __str__(self):
        return f"({self.bootcamp}, {self.course})"

    def __repr__(self):
        return f"{self.__class__.__name__}: ({self.bootcamp}, {self.course})"
