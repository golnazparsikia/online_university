from django.db import models
from django.utils.translation import gettext_lazy as _

from painless.models.mixins import TimestampMixin


class QuestionHelp(TimestampMixin):
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

    picture = models.ImageField(
        _("picture"),
        upload_to='elearning/warehouse/questionHelp',
        width_field='width_field',
        height_field='height_field',
        validators=[],
        null=True,
        blank=True,
        help_text=_("Image field for questionHelp"),
        db_comment="Image field for questionHelp"
    )

    alternate_text = models.CharField(
        _("Image Description"),
        max_length=100,
        help_text=_(
            "A description used when the main content, like an image, "
            "can't be shown."
        ),
    )

    width_field = models.IntegerField(
        _("Picture Width"),
        null=True,
        blank=True,
        help_text=_(
            "The horizontal size of an element, like an image, in numbers."
        ),
    )

    height_field = models.IntegerField(
        _("Picture Height"),
        null=True,
        blank=True,
        help_text=_(
            "The vertical size of an element, like an image, in numbers."
        ),
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _("Question Help")
        verbose_name_plural = _("Question Helps")

        db_table_comment = "Help section for questions."
        get_latest_by = ("created", "modified")

        default_manager_name = "objects"

    def __str__(self):
        return f"{self.id} Question Help"

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.id}"
