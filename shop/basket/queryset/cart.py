from django.db import models
from ..models.cart import Cart

class CartQueryset(models.Queryset):
    @staticmethod
    def get_all_carts():
        return Cart.objects.all()

    @staticmethod
    def get_cart_by_id(cart_id):
        return Cart.objects.filter(id=cart_id).first()

    @staticmethod
    def get_carts_for_user(user_id):
        return Cart.objects.filter(user_id=user_id)

    @staticmethod
    def get_carts_with_product(product_id):
        return Cart.objects.filter(product_id=product_id)

    @staticmethod
    def create_cart(slug, user, product):
        return Cart.objects.create(slug=slug, user=user, product=product)

    @staticmethod
    def update_cart(cart_id, slug, user, product):
        cart = CartQueryset.get_cart_by_id(cart_id)
        if cart:
            cart.slug = slug
            cart.user = user
            cart.product = product
            cart.save()
            return cart
        return None

    @staticmethod
    def delete_cart(cart_id):
        cart = CartQueryset.get_cart_by_id(cart_id)
        if cart:
            cart.delete()
            return True
        return False
