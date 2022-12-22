from decimal import Decimal

from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=64)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    @property
    def item_price(self) -> Decimal:
        return self.price * self.quantity

    def __str__(self) -> str:
        return f"{self.name}: (quantity:{self.quantity}, price: {self.price})"


class Order(models.Model):
    order_number = models.IntegerField(unique=True, primary_key=True)
    items = models.ManyToManyField(Item, related_name="orders")

    def __str__(self) -> str:
        return f"Order: {self.order_number}"

    @property
    def total_price(self) -> Decimal:
        return sum([item.item_price for item in self.items.objects.all()])
