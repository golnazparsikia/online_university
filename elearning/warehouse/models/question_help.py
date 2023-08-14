from django.db import models
from django.utils.translation import gettext_lazy as _

from painless.models.mixins import TimestampMixin


class QuestionHelp(TimestampMixin):
    #! create picture
    question = models.ForeignKey(
        "Question",
        on_delete=models.SET_NULL,
        verbose_name=_("Question"),
        related_name="question_helps",
        null=True,
        help_text=_(
            "Relates to the Question associated with this Question Help."
        ),
    )

    plain_text = models.CharField(
        _("Plain Text"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("The actual text of a question asked to users"),
    )

    html_code = models.CharField(
        _("HTML Code"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("The HTML code to display"),
    )

    code = models.CharField(
        _("Code Style"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Question with the code style."),
    )

    alternate_text = models.CharField(
        _("Image Description"),
        max_length=100,
        help_text=_(
            "A description used when the main content, like an image, "
            "can't be shown."
        ),
    )

    width_field = models.SmallIntegerField(
        _("Picture Width"),
        null=True,
        blank=True,
        help_text=_(
            "The horizontal size of an element, like an image, in numbers."
        ),
    )

    height_field = models.SmallIntegerField(
        _("Picture Height"),
        null=True,
        blank=True,
        help_text=_(
            "The vertical size of an element, like an image, in numbers."
        ),
    )

    class Meta:
        db_table_comment = "Help data for questions"
        get_latest_by = ("created", "modified")

    def __str__(self):
        return f"{self.question.product.title} Question Help"

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.question.product.title}"
