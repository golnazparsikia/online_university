from django.db import models
from django.db.models import Min, Max
from django.db.models import Count, Sum


class BasketQueryset(models.QuerySet):

    def get_cart_by_id(self, cart_id):
        return self.filter(id=cart_id).first()

    def get_carts_for_user(self, user_id):
        return self.filter(user_id=user_id)

    def get_carts_with_product(self, product_id):
        return self.filter(product_id=product_id)

    def create_cart(self, slug, user, product):
        return self.create(slug=slug, user=user, product=product)

    def update_cart(self, cart_id, slug, user, product):
        return self.filter(id=cart_id).update(slug=slug, user=user, product=product)

    def delete_cart(self, cart_id):
        return self.filter(id=cart_id).delete()

    def annotate_products_count(self):
        return self.annotate(num_products=Count('products'))

    def annotate_total_cost(self):
        return self.annotate(total_cost=Sum('products__cost'))

    def annotate_max_cart_cost_for_user(self):
        return self.values('user').annotate(max_cart_cost=Max('products__cost'))

    def annotate_min_cart_cost_for_user(self):
        return self.values('user').annotate(min_cart_cost=Min('products__cost'))

    def annotate_product_orders_count_for_cart(self):
        return self.annotate(num_product_orders=Count('product_orders'))

    def get_all_orders(self):
        return self.all()

    def get_order_by_transaction_num(self, transaction_number):
        return self.get(transaction_number=transaction_number)

    def get_orders_by_user_id(self, user_id):
        return self.filter(user_id=user_id)

    def get_orders_by_status(self, status):
        return self.filter(status=status)

    def get_orders_with_min_total_cost(self, min_total_cost):
        return self.filter(total_cost__gte=min_total_cost)

    def get_orders_sort_by_creation_date(self):
        return self.order_by('-created')

    def get_orders_with_admin_notes(self):
        return self.exclude(admin_note='')

    def annotate_active_orders_count_for_user(self):
        return self.values('user').annotate(num_active_orders=Count('user__orders', filter=models.Q(user__orders__status='Active')))

    def annotate_completed_orders_count_for_user(self):
        return self.values('user').annotate(num_completed_orders=Count('user__orders', filter=models.Q(user__orders__status='Completed')))

    def annotate_pending_orders_count_for_user(self):
        return self.values('user').annotate(num_pending_orders=Count('user__orders', filter=models.Q(user__orders__status='Pending')))

    def get_product_orders_by_order(self, order_id):
        return self.filter(order_id=order_id)

    def get_product_orders_by_product(self, product_id):
        return self.filter(product_id=product_id)

    def get_refunded_product_orders(self):
        return self.filter(is_refunded=True)

    def get_product_orders_with_min_cost(self, min_cost):
        return self.filter(cost__gte=min_cost)

    def get_latest_product_orders(self):
        return self.order_by('-created')

    def annotate_product_orders_count_for_cart(self):
        return self.values('order__user__id', 'product__cart__id').annotate(order_count=Count('order__user__id'))
