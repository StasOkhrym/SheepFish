from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=64)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.name}: (quantity:{self.quantity}, price: {self.price})"


class Order(models.Model):
    order_number = models.IntegerField(unique=True, primary_key=True)
    items = models.ForeignKey(Item, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"Order: {self.order_number}"
