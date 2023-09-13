from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from painless.models.mixins import (
    StockUnitMixin,
    TimestampMixin,
    PictureOperationAbstract
)

from ..helper.consts import Scope


class ProductMedia(PictureOperationAbstract,StockUnitMixin, TimestampMixin):

    product = models.ForeignKey(
        "Product",
        on_delete=models.PROTECT,
        verbose_name=_("Product"),
        related_name="medias",
        null=True,
        help_text=_("Relates to the product associated with this media."),
        db_comment=("How long something, like a video or audio, plays for.")
    )

    picture = models.ImageField(
        _("picture"),
        upload_to='elearning/warehouse/product_media',
        width_field='width_field',
        height_field='height_field',
        validators=[],
        null=True,
        blank=True,
        help_text=_("Image field for product"),
        db_comment="Image field for product"
    )

    video = models.FileField(
        _("video"),
        upload_to='elearning/warehouse/product_media',
        validators=[],
        null=True,
        blank=True,
        help_text=_("Video field for product"),
        db_comment="Video field for product"
    )

    pdf = models.FileField(
        _("pdf"),
        upload_to='elearning/warehouse/product_media',
        validators=[],
        null=True,
        blank=True,
        help_text=_("pdf field for product"),
        db_comment="pdf field for product"
    )

    alternate_text = models.TextField(
        _("Picture alt"),
        null=True,
        help_text=_("The descriptions of image."),
        db_comment=("The descriptions of image.")
    )

    duration = models.FloatField(
        _("Duration"),
        null=True,
        blank=True,
        help_text=_("How long something, like a video or audio, plays for."),
        db_comment=("How long something, like a video or audio, plays for.")
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _("Product Media")
        verbose_name_plural = _("Product Medias")

        db_table_comment = "Add media to product section."
        get_latest_by = ("created", "modified")

        default_manager_name = "objects"

    constraints = [
        models.CheckConstraint(
            check=~Q(product__scope=Scope.LESSON),
            name="valid_product"
        ),
    ]

    def clean(self):
        if self.product.scope == Scope.LESSON:
            raise ValidationError(
                {"product": "Lessons can not have product media."}
            )

    def __str__(self):
        return f"{self.id} Product Media"

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.id}"
