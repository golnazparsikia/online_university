from django.db import models
from django.utils.translation import gettext_lazy as _

from painless.models.mixins.common import (
    StockUnitMixin,
    TimestampMixin
)


class ProductMedia(StockUnitMixin,TimestampMixin):
    #! Create picture, video, pdf_file
    product = models.ForeignKey(
        "Product",
        on_delete=models.PROTECT,
        verbose_name=_("Product"),
        related_name="medias",
        null=True,
        help_text=_("Relates to the product associated with this media.")
    )

    alternate_text = models.CharField(
        _("Image Description"),
        max_length=50,
        help_text=_("A description used when the main content, like an image,"\
            "can't be shown.")
    )

    width_field = models.SmallIntegerField(
        _("Picture Width"),
        null=True,
        help_text=_("The horizontal size of an element, like an image, in numbers.")     # noqa: E501
    )

    height_field = models.SmallIntegerField(
        _("Picture Height"),
        null=True,
        help_text=_("The vertical size of an element, like an image, in numbers.")     # noqa: E501
    )

    duration = models.FloatField(
        _("Duration"),
        null=True,
        blank=True,
        help_text=_("How long something, like a video or audio, plays for.")
    )

    def __str__(self):
        return f"{self.product.title} Media"

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.product.title}"
