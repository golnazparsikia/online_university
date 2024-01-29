from django.db import models
from django.db.models import Min, Max
from django.db.models import Count, Sum

class BasketQueryset(models.QuerySet):
    """
    Custom queryset for managing baskets and orders.

    This queryset provides various methods for retrieving and manipulating shopping carts and orders.
    """

    def get_cart_by_id(self, cart_id):
        """
        Get a cart by its ID.

        Args:
            cart_id (int): The ID of the cart.

        Returns:
            Cart or None: The cart object if found, else None.
        """
        return self.filter(id=cart_id).first()

    def get_carts_for_user(self, user_id):
        """
        Get all carts for a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            QuerySet: A queryset of carts for the user.
        """
        return self.filter(user_id=user_id)

    def get_carts_with_product(self, product_id):
        """
        Get all carts containing a specific product.

        Args:
            product_id (int): The ID of the product.

        Returns:
            QuerySet: A queryset of carts containing the product.
        """
        return self.filter(product_id=product_id)

    def create_cart(self, slug, user, product):
        """
        Create a new cart.

        Args:
            slug (str): The slug for the cart.
            user (User): The user associated with the cart.
            product (Product): The product to add to the cart.

        Returns:
            Cart: The newly created cart.
        """
        return self.create(slug=slug, user=user, product=product)

    def update_cart(self, cart_id, slug, user, product):
        """
        Update an existing cart.

        Args:
            cart_id (int): The ID of the cart to update.
            slug (str): The new slug for the cart.
            user (User): The user associated with the cart.
            product (Product): The new product to add to the cart.

        Returns:
            int: The number of carts updated.
        """
        return self.filter(id=cart_id).update(slug=slug, user=user, product=product)

    def delete_cart(self, cart_id):
        """
        Delete a cart by its ID.

        Args:
            cart_id (int): The ID of the cart to delete.

        Returns:
            int: The number of carts deleted.
        """
        return self.filter(id=cart_id).delete()

    def annotate_products_count(self):
        """
        Annotate each cart with the count of products it contains.

        Returns:
            QuerySet: A queryset with the added 'num_products' attribute.
        """
        return self.annotate(num_products=Count('products'))

    def annotate_total_cost(self):
        """
        Annotate each cart with the total cost of its products.

        Returns:
            QuerySet: A queryset with the added 'total_cost' attribute.
        """
        return self.annotate(total_cost=Sum('products__cost'))

    def annotate_max_cart_cost_for_user(self):
        """
        Annotate each user with the maximum cost of products in their carts.

        Returns:
            QuerySet: A queryset with 'user' and 'max_cart_cost' attributes.
        """
        return self.values('user').annotate(max_cart_cost=Max('products__cost'))

    def annotate_min_cart_cost_for_user(self):
        """
        Annotate each user with the minimum cost of products in their carts.

        Returns:
            QuerySet: A queryset with 'user' and 'min_cart_cost' attributes.
        """
        return self.values('user').annotate(min_cart_cost=Min('products__cost'))

    def annotate_product_orders_count_for_cart(self):
        """
        Annotate each cart with the count of product orders associated with it.

        Returns:
            QuerySet: A queryset with the added 'num_product_orders' attribute.
        """
        return self.annotate(num_product_orders=Count('product_orders'))

    def get_all_orders(self):
        """
        Get all orders.

        Returns:
            QuerySet: A queryset containing all orders.
        """
        return self.all()

    def get_order_by_transaction_num(self, transaction_number):
        """
        Get an order by its transaction number.

        Args:
            transaction_number (str): The transaction number of the order.

        Returns:
            Order: The order object.
        """
        return self.get(transaction_number=transaction_number)

    def get_orders_by_user_id(self, user_id):
        """
        Get orders associated with a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            QuerySet: A queryset of orders for the user.
        """
        return self.filter(user_id=user_id)

    def get_orders_by_status(self, status):
        """
        Get orders with a specific status.

        Args:
            status (str): The status of the orders (e.g., 'Active', 'Completed', 'Pending').

        Returns:
            QuerySet: A queryset of orders with the specified status.
        """
        return self.filter(status=status)

    def get_orders_with_min_total_cost(self, min_total_cost):
        """
        Get orders with a total cost greater than or equal to a specified minimum.

        Args:
            min_total_cost (float): The minimum total cost for orders.

        Returns:
            QuerySet: A queryset of orders meeting the criteria.
        """
        return self.filter(total_cost__gte=min_total_cost)

    def get_orders_sort_by_creation_date(self):
        """
        Get orders sorted by their creation date in descending order.

        Returns:
            QuerySet: A queryset of orders sorted by creation date.
        """
        return self.order_by('-created')

    def get_orders_with_admin_notes(self):
        """
        Get orders that have admin notes.

        Returns:
            QuerySet: A queryset of orders with admin notes.
        """
        return self.exclude(admin_note='')

    def annotate_active_orders_count_for_user(self):
        """
        Annotate each user with the count of active orders they have.

        Returns:
            QuerySet: A queryset with 'user' and 'num_active_orders' attributes.
        """
        return self.values('user').annotate(num_active_orders=Count('user__orders', filter=models.Q(user__orders__status='Active')))

    def annotate_completed_orders_count_for_user(self):
        """
        Annotate each user with the count of completed orders they have.

        Returns:
            QuerySet: A queryset with 'user' and 'num_completed_orders' attributes.
        """
        return self.values('user').annotate(num_completed_orders=Count('user__orders', filter=models.Q(user__orders__status='Completed')))

    def annotate_pending_orders_count_for_user(self):
        """
        Annotate each user with the count of pending orders they have.

        Returns:
            QuerySet: A queryset with 'user' and 'num_pending_orders' attributes.
        """
        return self.values('user').annotate(num_pending_orders=Count('user__orders', filter=models.Q(user__orders__status='Pending')))

    def get_product_orders_by_order(self, order_id):
        """
        Get product orders associated with a specific order.

        Args:
            order_id (int): The ID of the order.

        Returns:
            QuerySet: A queryset of product orders for the order.
        """
        return self.filter(order_id=order_id)

    def get_product_orders_by_product(self, product_id):
        """
        Get product orders associated with a specific product.

        Args:
            product_id (int): The ID of the product.

        Returns:
            QuerySet: A queryset of product orders for the product.
        """
        return self.filter(product_id=product_id)

    def get_refunded_product_orders(self):
        """
        Get product orders that have been refunded.

        Returns:
            QuerySet: A queryset of refunded product orders.
        """
        return self.filter(is_refunded=True)

    def get_product_orders_with_min_cost(self, min_cost):
        """
        Get product orders with a cost greater than or equal to a specified minimum.

        Args:
            min_cost (float): The minimum cost for product orders.

        Returns:
            QuerySet: A queryset of product orders meeting the criteria.
        """
        return self.filter(cost__gte=min_cost)

    def get_latest_product_orders(self):
        """
        Get the latest product orders, sorted by creation date in descending order.

        Returns:
            QuerySet: A queryset of the latest product orders.
        """
        return self.order_by('-created')

    def annotate_product_orders_count_for_cart(self):
        """
        Annotate each cart with the count of product orders associated with it.

        Returns:
            QuerySet: A queryset with the added 'order_count' attribute.
        """
        return self.values('order__user__id', 'product__cart__id').annotate(order_count=Count('order__user__id'))
