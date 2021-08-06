from django.db import models

from django.conf import settings
from mainapp.models import Product

class Order(models.Model):
    FORMING = 'FM'
    SEND_TO_PROCEED = 'STP'
    PROCEED = 'PR'
    PAID = 'PD'
    READY = 'RDY'
    CENCEL = 'CNC'

    order_status_chose = (
        (FORMING, 'формирование'),
        (SEND_TO_PROCEED,  'отправлен в обработку'),
        (PROCEED, 'обработан'),
        (PAID, 'оплачено'),
        (READY, 'готово'),
        (CENCEL, 'отменено')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    update = models.DateTimeField(verbose_name='обнавлен', auto_now_add=True)
    status = models.CharField(verbose_name='статус', max_length=3, choices=order_status_chose, default=FORMING),
    is_activ = models.BooleanField(verbose_name='активный', default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
    def __str__(self):
        return 'Текущий заказ {}'.format(self.id)

    def get_total_quantity(self):
        items = self.orderitmes.select_related
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.orderitems.select_related
        return len(items)

    def get_total_cost(self):
        items = self.orderitems.select_related
        return sum(list(map(lambda x: x.quantity*x.product.price, items)))

    def delete(self):
        for item in self.orderitem.select_related:
            item.product.quantity =+ item.quantity
            item.product.save()
        self.is_activ = False
        self.save()

class OrderItem(models.Model):
    objects = OrderItemQuerySet.as_manager()
    order = models.ForeignKey(Order, related_name="orderitems", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='продукт', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)

    def get_product_cost(self):
        return self.product * self.quantity

    def delete(self):
        self.product.quantity += self.quantity
        self.product.save()
        super(self.__class__, self).delete()


class OrderItemQuerySet(models.QuerySet):

   def delete(self, *args, **kwargs):
       for object in self:
           object.product.quantity += object.quantity
           object.product.save()
       super(OrderItemQuerySet, self).delete(*args, **kwargs)

