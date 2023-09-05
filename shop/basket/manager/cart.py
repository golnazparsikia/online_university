from django.db import models
from ..models.cart import Cart
from ..queryset.cart import CartQuerySet

class CartDataAccessLayer(models.Manager):
    def get_query_set(self):
        return CartQuerySet(self.model, using=self._db)

    def with_active_otp_count(self):
        return self.get_query_set().with_active_otp_count()

    def with_total_price(self):
        return self.get_query_set().with_total_price()

    def filter_by_user(self, user):
        return self.get_query_set().filter_by_user(user)

    def filter_by_product(self, product):
        return self.get_query_set().filter_by_product(product)

    def filter_by_active_otp_count(self, min_active_otp_count=1):
        return self.get_query_set().filter_by_active_otp_count(min_active_otp_count)

    def filter_by_total_price(self, min_total_price=0):
        return self.get_query_set().filter_by_total_price(min_total_price)
