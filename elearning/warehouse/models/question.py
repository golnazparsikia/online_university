from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from painless.models.mixins import TimestampMixin, DescriptionMixin
from elearning.warehouse.helper.consts import Scope, QuestionType


class Question(TimestampMixin, DescriptionMixin):
    product = models.ForeignKey(
        "Product",
        on_delete=models.PROTECT,
        verbose_name=_("Product"),
        related_name="questions",
        null=True,
        limit_choices_to={"scope": Scope.CHAPTER},
        help_text=_("Relates to the product associated with this question."),
    )

    text = models.CharField(
        _("Question text"),
        max_length=255,
        help_text=_("The actual text of a question asked to users."),
    )

    kind = models.CharField(
        _("Question Type"),
        max_length=20,
        choices=QuestionType.choices,
        help_text=_("Varieties of question formats."),
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

        db_table_comment = "The question section is for the product."
        get_latest_by = ("created", "modified")

        default_manager_name = "objects"

        constraints = [
            models.CheckConstraint(
                check=Q(kind__in=QuestionType.values),
                name="valid_question_kind"
            )
        ]

    def __str__(self):
        return f"{self.id} Question"

    def __repr__(self):
        return f"{self.id} Question"
