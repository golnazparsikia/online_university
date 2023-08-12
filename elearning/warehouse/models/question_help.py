from django.db import models
from django.utils import timezone

from painless.models.mixins import (
    TimeStampMixin,
    )

class QuestionHelp(TimeStampMixin):
    id = models.AutoField(
        primary_key=True
        )
    question = models.ForeignKey(
        'Question',
        on_delete=models.PROTECT,
        null=False,
        related_name='help',
        help_text='Question related question help'
    )
    plain_text = models.TextField(
        null=True,
        blank=True,
        help_text='Simple question text'
    )
    html_code = models.TextField(
        null=True,
        blank=True,
        help_text='HTML code to display'
    )
    code = models.TextField(
        null=True,
        blank=True,
        help_text='Question with code style'
    )
    # picture = models.ImageField(
    #     null=True,
    #     blank=True,
    #     upload_to='question_help/',
    #     max_length=100,
    #     help_text='Photo supports jpg, jpeg, png format, this field can be empty'
    # )
    alternate_text = models.CharField(
        max_length=100,
        null=False,
        help_text='Description of the image'
    )
    width_field = models.IntegerField(
        null=True,
        help_text='Width of the picture'
    )
    height_field = models.IntegerField(
        null=True,
        help_text='Height of the picture'
    )
    
    def __str__(self):
        return self.question
    
    def __repr__(self):
        return self.question
    class Meta:
        db_table = 'warehouse_question_help'
        verbose_name = 'Question Help'
        verbose_name_plural = 'Question Helps'