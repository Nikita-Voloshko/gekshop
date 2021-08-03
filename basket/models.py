from django.db import models
from authapp.models import User
from mainapp.models import Product
# Create your models here.


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    get_items = models.CharField()

    def __str__(self):
        return f'Корзина для {self.User.username} | {self.Product.name}'


def sum(self):
    return self.quantity * self.product.price


def get_items(self, user):
    item = Basket.objects.get(user=user)
    return item

    def total_quantity(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.quantity for basket in baskets)

    def total_sum(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.sum() for basket in baskets)
