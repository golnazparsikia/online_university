from django.db import models

from painless.models.mixins import (
    TimeStampMixin,
    )

class Answer(TimeStampMixin):
    id = models.AutoField(
        primary_key=True
        )
    question = models.ForeignKey(
        'Question',
        on_delete=models.PROTECT,
        null=False,
        related_name='answers',
        help_text='Related to which question'
    )
    text = models.TextField(
        null=False,
        help_text='The text of the answer is unlimited'
    )
    is_correct = models.BooleanField(
        null=False,
        help_text='The correct answer to the question'
    )
    priority = models.IntegerField(
        unique=True,
        null=False,
        help_text='Prioritization'
    )
    order_placeholder = models.IntegerField(
        null=True,
        blank=True,
        help_text='The order of display elements'
    )
    def __str__(self):
        return self.question
    
    def __repr__(self):
        return self.question
    
    class Meta:
        db_table = 'warehouse_answer'
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'