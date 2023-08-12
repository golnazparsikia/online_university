import uuid
import enum
from django.db import models
from django.utils.text import slugify
from django.utils import timezone

from painless.models.mixins import (
    TimeStampMixin,
    StockunitMixin,
    TitleSlugMixin
    )


class Question(TimeStampMixin):

    class QuestionTypes(models.TextChoices):
        CHECKBOX = 'checkbox'
        RADIO = 'radio'
        PLACEHOLDER = 'placeholder'
        CONDITIONAL = 'conditional'
        CODE = 'code'
        
    id = models.AutoField(
        primary_key=True
        )
    product = models.ForeignKey(
        'Product', 
        on_delete=models.PROTECT, 
        null=True, 
        related_name='questions', 
        help_text='Product related question'
    )
    text = models.CharField(
        max_length=255, 
        help_text='Question text maximum 255 characters'
        )
    kind = models.CharField(
        max_length=100, 
        choices=QuestionTypes.choices, 
        help_text='Question type'
        )
    description = models.TextField(
        null=True, 
        blank=True, 
        help_text='Description of the question without restrictions'
        )
    def __str__(self):
        return self.kind
    
    def __repr__(self):
        return self.kind
    class Meta:
        db_table = 'warehouse_question'
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'