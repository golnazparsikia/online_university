from django.db import models
from django.utils.text import slugify
from painless.models.mixins import (
    TimeStampMixin,
    StockunitMixin,
    )


class ProductMedia(TimeStampMixin,StockunitMixin):

    id = models.AutoField(
        primary_key=True
        )
    
    product = models.ForeignKey(
        'Product', 
        on_delete=models.PROTECT, 
        null=True, 
        related_name='product_medias',
        verbose_name='Product',
        help_text="Which product does the media belong to?"
        )
    # picture = models.ImageField(
    #     upload_to='product_media/', 
    #     null=True, 
    #     blank=True, 
    #     help_text="Photo supports jpg, jpeg, png format, this field can be empty"
    #     )
    alternate_text = models.CharField(
        max_length=100, 
        null=True, 
        help_text="Description of the image"
        )
    width_field = models.IntegerField(
        null=True, 
        help_text="Width of the picture"
        )
    height_field = models.IntegerField(
        null=True, 
        help_text="Height of the picture"
        )
    slug = models.SlugField(
        verbose_name='Slug',
        max_length=255,
        unique=False,
        null=True,
        allow_unicode =True,
        help_text='Slug is a news paper term, A short label for'
    )

    # video = models.FileField(
    #     upload_to='product_media/', 
    #     null=True, 
    #     blank=True, 
    #     help_text="Photo supports mp4, mov, mkv format, this field can be empty"
    #     )
    duration = models.DurationField(
        null=True, 
        blank=True, 
        help_text="The duration of the video, which can be a decimal"
        )
    
    # pdf = models.FileField(
    #     upload_to='product_media/', 
    #     null=True, 
    #     blank=True, 
    #     help_text="Document file that can be empty"
    #     )
    
    def __str__(self):
        return f"ProductMedia ID: {self.id}"
    
    def __repr__(self):
        return f"ProductMedia ID: {self.id}"
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.duration, allow_unicode=True)
        super().save(*args,**kwargs)
    class Meta:
        db_table = 'warehouse_productmedia'
        verbose_name = 'Productmedia'
        verbose_name_plural = 'Productmedias'

