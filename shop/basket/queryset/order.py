from django.db import models
from ..models.order import Order

class OrderQueryset(models.QuerySet):
    @staticmethod
    def get_all_orders():
        qs= Order.objects.all()
        return qs
    
    @staticmethod
    def get_order_by_transaction_num(transaction_number):
        qs= Order.objects.get(transaction_number=transaction_number)
        return qs
    
    @staticmethod
    def get_order_by_user_id(user_id):
        qs = Order.objects.filter(user_id=user_id)
        return qs
    
    @staticmethod
    def get_order_by_status(status):
        qs = Order.objects.filter(status=status)
        return qs

    @staticmethod
    def get_order_by_user(user_id):
        qs = Order.objects.filter(user_id=user_id)
        return qs
    
    @staticmethod
    def get_orders_with_min_total_cost(min_total_cost):
        qs= Order.objects.filter(total_cost__gte=min_total_cost)
        return qs
    

    @staticmethod
    def get_orders_sort_by_creation_date():
        qs = Order.objects.order_by('-created')
        return qs

    @staticmethod
    def get_orders_admin_notes():
        qs= Order.objects.exclude(admin_note='')
        return qs

