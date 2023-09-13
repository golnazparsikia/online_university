from django.db import models
from django.utils.translation import gettext_lazy as _

from painless.models.mixins import TimestampMixin
from account.auth.models.user import User
from ..helper.consts import status

class Order(TimestampMixin):
    
    transaction_number = models.CharField(
        _("Number of transaction"),
        max_length=255,
        help_text=_("Unique identifier for the transaction."),
        db_comment=_("Unique identifier for the transaction.")
        )

    status = models.CharField(
        _("Status"),
        max_length=255,
        choices=status.choices,
        default=status.ACTIVE, 
        help_text=_("Current status of the order."),
        db_comment=_("Current status of the order.")
        )

    admin_note = models.TextField(
        _("Admin note"),
        blank=True,
        null=True,
        help_text=_("Optional note added by an administrator."),
        db_comment=_("Optional note added by an administrator.")
        )

    total_cost = models.DecimalField(
        _("Total cost"),
        max_digits=10,
        decimal_places=2,
        help_text=_("Total cost of the order."),
        db_comment=_("Total cost of the order.")
        )  

    user = models.ForeignKey(
        User,
        related_name="orders",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        help_text=_("User who placed the order."),
        db_comment=_("User who placed the order.")
        )

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ("-created",)

    def __str__(self):
        return f"Order {self.transaction_number}"

    def __repr__(self):
        return f"Order {self.transaction_number}"
