from decimal import Decimal

from django.conf import settings
from django.db import models

# Create your models here.


class CartItem(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name

    def total(self) -> Decimal:
        return self.product.price * self.quantity


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.user.username

    def total(self) -> float:
        """
        Calculates the total price of all the items in the cart.
        """

        total = 0
        for item in self.items.all():
            total += item.product.price * item.quantity

        return total

    def __unicode__(self) -> str:
        return "Cart id: %s" % self.id

    def clear(self):
        self.items.clear()
        self.save()

    def add_to_cart(self, product, quantity=1):
        """
        Adds a product to the cart.
        If the product is already in the cart then its quantity will be updated.

        :param product: The product to add.
        :param quantity: The quantity of the product to add.

        :return: None
        """

        cart = self
        new_item, _ = CartItem.objects.get_or_create(product=product, quantity=quantity)
        if new_item not in cart.items.all():
            cart.items.add(new_item)
            cart.save()

        else:
            for item in cart.items.all():
                if item.product == product:
                    item.quantity += quantity
                    item.save()
                    cart.save()

    def remove_from_cart(self, product) -> bool:
        """
        Removes a product from the cart.

        :param product: The product to remove.

        :return: True if the product was removed, False otherwise.
        """

        cart = self
        for cart_item in cart.items.all():
            if cart_item.product == product:
                cart.items.remove(cart_item)
                cart.save()

                return True

        return False

    def remove_from_cart_by_id(self, id) -> bool:
        """
        Removes a product from the cart by its id.

        :param id: The id of the product to remove.

        :return: True if the product was removed, False otherwise.
        """

        cart = self
        for cart_item in cart.items.all():
            if cart_item.id == id:
                cart.items.remove(cart_item)
                cart.save()

                return True

        return False

    def remove_from_cart_by_index(self, index):
        self.items.remove(self.items.all()[index])
        self.save()

        return True
