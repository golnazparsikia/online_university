from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from account.auth.models.user import User
from elearning.warehouse.models.product import Product
from painless.models.mixins import TimestampMixin

class Cart(TimestampMixin):

    slug = models.SlugField(
        _("Slug"),
        max_length=255,
        unique=True,
        help_text=_(
            "A URL-friendly version of the title, typically used in"
            "the URL to identify the content's location."
        ),
    )

    # Useful when subclass doesn't override save.
    def save(self, *args, **kwargs):
        self.slug = slugify(self.user, allow_unicode=True)
        super().save(*args, **kwargs)

    user = models.ForeignKey(
        User,
        related_name="carts",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        help_text=_("The user associated with this cart."),
        db_comment=("The user associated with this cart.")
    )

    product = models.ForeignKey(
        Product,
        related_name="carts",
        verbose_name=_("Product"),
        on_delete=models.DO_NOTHING,
        help_text=_("The product associated with this cart."),
        db_comment=("The product associated with this cart.")
    )

    def __str__(self):
        return self.product

    def __repr__(self):
        return self.product
    
    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")