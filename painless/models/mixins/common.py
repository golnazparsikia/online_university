from django.db import models
from django.utils.text import slugify
import uuid

class TimeStampMixin(models.Model):
    
    created = models.DateTimeField(
        verbose_name='Created',
        auto_now_add=True,
        help_text='Date and time of record creation'
    )
    
    modified = models.DateTimeField(
        verbose_name='Modified',
        auto_now=True,
        help_text='Date and time of record modification'
    )

    class Meta:
        abstract = True

class StockunitMixin(models.Model):
    sku = models.CharField(
        verbose_name='SKU',
        default=uuid.uuid4,
        max_length=100,
        unique=True,
        null=False,
        help_text='Product ID serial, maximum 50 characters'
    )
    
    class Meta:
        abstract = True

class TitleSlugMixin(models.Model):
    title = models.CharField(
        verbose_name='Title',
        max_length=255,
        unique=False,
        null=True,
        help_text='Product title is unique and maximum 255 characters'
    )
    
    slug = models.SlugField(
        verbose_name='Slug',
        max_length=255,
        unique=False,
        null=True,
        allow_unicode =True,
        help_text='Slug is a news paper term, A short label for'
    )

    class Meta:
        abstract = True