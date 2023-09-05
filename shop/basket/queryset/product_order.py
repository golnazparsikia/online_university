from django.db import models
from ..models.product_order import ProductOrder

class ProductOrderQueryset(models.QuerySet):
    @staticmethod
    def get_all_products():
        qs= ProductOrder.objects.all()
        return
    @staticmethod
    def get_product_orders_by_order(order_id):
        qs=ProductOrder.objects.filter(order_id=order_id)
        return
    @staticmethod
    def get_product_orders_by_product(product_id):
        qs= ProductOrder.objects.filter(product_id=product_id)
        return
    @staticmethod
    def get_refunded_product_orders():
        qs= ProductOrder.objects.filter(is_refunded=True)
        return
    @staticmethod
    def get_product_orders_with_min_cost(min_cost):
        qs= ProductOrder.objects.filter(cost__gte=min_cost)
        return
    @staticmethod
    def get_latest_product_orders():
        qs= ProductOrder.objects.order_by('-created')
        return