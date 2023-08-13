import uuid

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class TitleSlugMixin(models.Model):
    title = models.CharField(
        _("Title"),
        max_length=255,
        unique=True,
        help_text=_("The main textual identifier or name for the content")
    )

    slug = models.SlugField(
        _("Slug"),
        max_length=255,
        unique=True,
        help_text=_("A URL-friendly version of the title, typically used in"\
                    "the URL to identify the content's location.")
    )

    # Useful when subclass doesn't override save.
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save( *args, **kwargs)

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    created = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        help_text=_("The timestamp indicating when the model instance was"\
                    "initially added or created.")
    )

    modified = models.DateTimeField(
        _("Modified at"),
        auto_now=True,
        help_text=_("The timestamp representing the most recent update or"\
                    "modification to the model instance.")
    )

    class Meta:
        abstract=True


class StockUnitMixin(models.Model):
    sku = models.UUIDField(
        _("Stock of Unit"),
        max_length=100,
        default=uuid.uuid4,
        unique=True,
        help_text=_("A unique identifier assigned to each product in inventory.")    # noqa: E501
    )

    class Meta:
        abstract=True


class DescriptionMixin(models.Model):
    description = models.TextField(
        _("Description"),
        null=True,
        blank=True,
        help_text=_("A textual explanation or summary providing additional"\
            "information about the item's characteristics or purpose.")
    )

    class Meta:
        abstract=True
