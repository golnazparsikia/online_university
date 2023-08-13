from django.db import models
from django.utils.translation import gettext_lazy as _

from painless.models.mixins.common import TimestampMixin


class Answer(TimestampMixin):
    question = models.ForeignKey(
        "Question",
        on_delete=models.PROTECT,
        verbose_name=_("Question"),
        related_name="answers",
        null=True,
        help_text=_("Relates to the Question associated with this answer.")
    )

    text = models.TextField(
        _("Text"),
        help_text=_("The text of the answer.")
    )

    is_correct = models.BooleanField(
        _("Is Correct?"),
        help_text=_("The correct answer to the question"),
    )

    priority = models.PositiveIntegerField(
        _("Priority"),
        unique=True,
        help_text=_("Ranking items based on importance for resource"\
                    "allocation and decision-making.")
    )

    order_placeholder = models.PositiveIntegerField(
        _("Display Order"),
        null=True,
        blank=True,
        help_text=_("The order of displaying elements.")
    )

    def __str__(self):
        return f"{self.question.product.title} Question Answer"
    
    def __repr__(self):
        return f"{self.__class__.__name__}: {self.question.product.title} Question"
