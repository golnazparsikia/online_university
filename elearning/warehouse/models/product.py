import uuid

from django.db import models
from django.utils.text import slugify

from painless.models.mixins import (
    TimeStampMixin,
    StockunitMixin,
    TitleSlugMixin
    )


class Product(TimeStampMixin,StockunitMixin,TitleSlugMixin):
    
    id = models.AutoField(
        primary_key=True,
        )
    
    parent = models.ForeignKey(
        'self',
        verbose_name='Parent',
        null=True,
        on_delete=models.PROTECT,
        blank=True,
        # related_name='products',#!qa
        related_name='children',
        help_text='Product subcategory'
    )
    
    scope = models.CharField(
        verbose_name='Scope',
        max_length=255,
        null=True,
        help_text='Record track basin'
    )
    
    description = models.TextField(
        verbose_name='Description',
        null=True,
        blank=True,
        help_text='Text for the description of the scope'
    )
    
    is_buyable = models.BooleanField(
        verbose_name='Is Buyable',
        default=False,
        help_text='Can be sold or not'
    )
    
    bundle = models.ForeignKey(
        'self',
        verbose_name='Bundle',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='products',
        help_text='Course connection to bootcamp'
    )
    
    experience = models.IntegerField(
        verbose_name='Experience',
        null=False,
        help_text='Level of satisfaction and experience'
    )
    
    difficulty = models.CharField(
        verbose_name='Difficulty',
        max_length=255,
        null=True,
        help_text='The hardness of the product'
    )
    
    priority = models.IntegerField(
        verbose_name='Priority',
        null=False,
        help_text='Product prioritization'
    )
    
    
    def __str__(self):
        return self.title
    
    def __repr__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args,**kwargs)

    class Meta:
        db_table = 'warehouse_product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
