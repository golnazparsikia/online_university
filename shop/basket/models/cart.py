from django.db import models
from django.utils.translation import gettext_lazy as _

from account.auth.models.user import User
from elearning.warehouse.models.product import Product
from painless.models.mixins import TimestampMixin

class Cart(TimestampMixin):

    slug = models.CharField(
        max_length=255,
        help_text=_("A unique identifier for the cart.")
    )

    user = models.ForeignKey(
        User,
        related_name="carts",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        help_text=_("The user associated with this cart.")
    )
    
    product = models.ForeignKey(
    Product,
    related_name="carts",
    verbose_name=_("Product"),
    on_delete=models.DO_NOTHING,
    help_text=_("The product associated with this cart.")
)

    def __str__(self):
        return f"Cart {self.id} - {self.user}"

    def __repr__(self):
        return f"Cart(id={self.id}, user={self.user.username}, product={self.product})"
    
    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")