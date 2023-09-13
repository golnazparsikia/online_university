from django.db import models
from ..queryset.cart import CartQueryset


class CartDataAccessLayer(models.Manager):
    def get_query_set(self):
        return CartQueryset(self.model, using=self._db)

    def get_cart_by_id(self, cart_id):
        return self.get_query_set().get_cart_by_id(cart_id)

    def get_carts_for_user(self, user_id):
        return self.get_query_set().get_carts_for_user(user_id)

    def get_carts_with_product(self, product_id):
        return self.get_query_set().get_carts_with_product(product_id)

    def create_cart(self, slug, user, product):
        return self.get_query_set().create_cart(slug, user, product)

    def delete_cart_by_product_id(self, product_id):
        return self.get_query_set().delete_cart_by_product_id(product_id)
