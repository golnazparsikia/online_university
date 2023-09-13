from django.db import models
from ..queryset.basket_queryset import BasketQueryset

class BasketDataAccessLayer(models.Manager):
    """
    Data access layer for managing baskets and orders.
    This class provides methods for accessing and manipulating shopping carts, orders, and product orders.
    """
    class CartDataAccessLayer(models.Manager):
        def get_query_set(self):
            return BasketQueryset(self.model, using=self._db)

        def get_cart_by_id(self, cart_id):
            return self.get_query_set().get_cart_by_id(cart_id)

        def get_carts_for_user(self, user_id):
            return self.get_query_set().get_carts_for_user(user_id)

        def get_carts_with_product(self, product_id):
            return self.get_query_set().get_carts_with_product(product_id)

        def create_cart(self, slug, user, product):
            return self.get_query_set().create_cart(slug, user, product)

        def update_cart(self, cart_id, slug, user, product):
            return self.get_query_set().update_cart(cart_id, slug, user, product)

        def delete_cart(self, cart_id):
            return self.get_query_set().delete_cart(cart_id)

        def annotate_products_count(self):
            return self.get_query_set().annotate_products_count()

        def annotate_total_cost(self):
            return self.get_query_set().annotate_total_cost()

        def annotate_max_cart_cost_for_user(self):
            return self.get_query_set().annotate_max_cart_cost_for_user()

        def annotate_min_cart_cost_for_user(self):
            return self.get_query_set().annotate_min_cart_cost_for_user()

        def annotate_product_orders_count_for_cart(self):
            return self.get_query_set().annotate_product_orders_count_for_cart()


    class OrderDataAccessLayer(models.Manager):
        def get_query_set(self):
            return BasketQueryset(self.model, using=self._db)

        def get_all_orders(self):
            return self.get_query_set().get_all_orders()

        def get_order_by_transaction_num(self, transaction_number):
            return self.get_query_set().get_order_by_transaction_num(transaction_number)

        def get_orders_by_user_id(self, user_id):
            return self.get_query_set().get_orders_by_user_id(user_id)

        def get_orders_by_status(self, status):
            return self.get_query_set().get_orders_by_status(status)

        def get_orders_with_min_total_cost(self, min_total_cost):
            return self.get_query_set().get_orders_with_min_total_cost(min_total_cost)

        def get_orders_sort_by_creation_date(self):
            return self.get_query_set().get_orders_sort_by_creation_date()

        def get_orders_with_admin_notes(self):
            return self.get_query_set().get_orders_with_admin_notes()

        def annotate_active_orders_count_for_user(self):
            return self.get_query_set().annotate_active_orders_count_for_user()

        def annotate_completed_orders_count_for_user(self):
            return self.get_query_set().annotate_completed_orders_count_for_user()

        def annotate_pending_orders_count_for_user(self):
            return self.get_query_set().annotate_pending_orders_count_for_user()


    class ProductOrderDataAccessLayer(models.Manager):
        def get_query_set(self):
            return BasketQueryset(self.model, using=self._db)

        def get_all_products(self):
            return self.get_query_set().get_all_products()

        def get_product_orders_by_order(self, order_id):
            return self.get_query_set().get_product_orders_by_order(order_id)

        def get_product_orders_by_product(self, product_id):
            return self.get_query_set().get_product_orders_by_product(product_id)

        def get_refunded_product_orders(self):
            return self.get_query_set().get_refunded_product_orders()

        def get_product_orders_with_min_cost(self, min_cost):
            return self.get_query_set().get_product_orders_with_min_cost(min_cost)

        def get_latest_product_orders(self):
            return self.get_query_set().get_latest_product_orders()

        def annotate_product_orders_count_for_cart(self):
            return self.get_query_set().annotate_product_orders_count_for_cart()
