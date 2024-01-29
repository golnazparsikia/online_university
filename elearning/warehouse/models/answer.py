from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from painless.models.mixins import TimestampMixin
from ..helper.consts import QuestionType


class Answer(TimestampMixin):
    question = models.ForeignKey(
        "Question",
        on_delete=models.PROTECT,
        verbose_name=_("Question"),
        related_name="answers",
        null=True,
        help_text=_("Relates to the Question associated with this answer."),
    )
    text = models.TextField(_("Text"), help_text=_("The text of the answer."))
    is_correct = models.BooleanField(
        _("Is Correct?"),
        help_text=_("The correct answer to the question"),
    )
    priority = models.PositiveIntegerField(
        _("Priority"),
        unique=False,
        null=True,
        help_text=_(
            "Ranking items based on importance for resource"
            "allocation and decision-making."
        ),
    )
    order_placeholder = models.PositiveIntegerField(
        _("Display Order"),
        null=True,
        blank=True,
        help_text=_("The order of displaying elements."),
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")

        db_table_comment = "Write the answer according to the question."
        get_latest_by = ("created", "modified")

        default_manager_name = "objects"

        constraints = [
            models.UniqueConstraint(
                fields=["question", "order_placeholder"],
                condition=~Q(order_placeholder=None),
                name="unique_order_placeholder"
            )
        ]

    def clean(self):
        if self.question.kind != QuestionType.PLACEHOLDER and self.order_placeholder != None:
            raise ValidationError(
                {"order_placeholder": "Questions other than placeholders should have None for placeholders."}
            )

        if self.question.kind == QuestionType.PLACEHOLDER:
            existing_records = self.__class__.objects.exclude(pk=self.pk).filter(
                question=self.question,
                order_placeholder=self.order_placeholder
            )
            if existing_records.exists():
                raise ValidationError(
                    {"order_placeholder": _("This order_placeholder for this question is duplicated.")}
                )

        if self.question.kind in (QuestionType.RADIO, QuestionType.CONDITIONAL):
            existing_records = self.__class__.objects.exclude(pk=self.pk).filter(
                question=self.question,
                is_correct=True
            )
            if existing_records.exists():
                raise ValidationError(
                    {"is_correct": "Only 1 correct answer is ok for radio and conditional question type."}
                )

        if self.question.kind == QuestionType.CODE:
            existing_records = self.__class__.objects.exclude(pk=self.pk).filter(
                question=self.question,
            )
            if existing_records.exists():
                raise ValidationError(_("It should be just 1 answer for code type questions."))
            if self.is_correct is False:
                raise ValidationError(
                    {"is_correct": "The answer should be correct for the code type question."}
                )

    def __str__(self):
        return f"{self.id} Answer"
    def __repr__(self):
        return f"{self.__class__.__name__}: {self.id}"


class Checkbox(Answer):
    """Proxy model representing a Checkbox."""
    class Meta:
        proxy = True,
        verbose_name = _("Checkbox"),
        verbose_name_plural = _("Checkboxes")

class Radio(Answer):
    """Proxy model representing a Radio."""
    class Meta:
        proxy = True,
        verbose_name = _("Radio"),
        verbose_name_plural = _("Radios")

class Placeholder(Answer):
    """Proxy model representing a Placeholder."""
    class Meta:
        proxy = True,
        verbose_name = _("Placeholder"),
        verbose_name_plural = _("Placeholder")

class Conditional(Answer):
    """Proxy model representing a Conditional."""
    class Meta:
        proxy = True,
        verbose_name = _("Conditional"),
        verbose_name_plural = _("Conditionals")

class Code(Answer):
    """Proxy model representing a Code."""
    class Meta:
        proxy = True,
        verbose_name = _("Code"),
        verbose_name_plural = _("Codes")
