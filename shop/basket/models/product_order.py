from django.db import models
from django.utils.translation import gettext_lazy as _

from painless.models.mixins import TimestampMixin
from shop.basket.models.order import Order
from elearning.warehouse.models.product import Product


class ProductOrder(TimestampMixin):

    cost = models.DecimalField(
        _("Cost"),
        max_digits=10,
        decimal_places=2,
        help_text="The cost of the product order.",
        db_comment=("The cost of the product order.")
    )

    is_refunded = models.BooleanField(
        ("Is_refunded"),
        help_text=("Indicates whether the product order has been refunded."),
        db_comment=("Indicates whether the product order has been refunded.")
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="product_orders",
        verbose_name=_("Order"),
        help_text=_("The order to which this product order belongs."),
        db_comment=("The order to which this product order belongs.")
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_orders",
        verbose_name=_("Product"),
        help_text=_("The product associated with this product order."),
        db_comment=("The product associated with this product order.")
    )

    class Meta:
        verbose_name = _("Product_Order")
        verbose_name_plural = _("Product_Orders")
        ordering = ("-created",
    )

    def __str__(self):
        return f"ProductOrder {self.id}"

    def __repr__(self):
        return f"ProductOrder {self.id}"
