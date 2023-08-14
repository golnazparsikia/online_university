from django.db import models
from django.utils.translation import gettext_lazy as _

from painless.models.mixins import TimestampMixin, DescriptionMixin
from elearning.warehouse.helper.consts import QUESTIONTYPES


class Question(TimestampMixin, DescriptionMixin):
    product = models.ForeignKey(
        "Product",
        on_delete=models.PROTECT,
        verbose_name=_("Product"),
        related_name="questions",
        null=True,
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
        choices=QUESTIONTYPES.choices,
        help_text=_("Varieties of question formats."),
    )

    class Meta:
        get_latest_by = ("created", "modified")

    def __str__(self):
        return f"{self.product.title} Question"

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.product.title}"
