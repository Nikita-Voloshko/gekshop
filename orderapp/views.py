from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction

from django.forms import inlineformset_factory
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from basket.models import Basket
from orderapp.models import Order, OrderItem
from orderapp.forms import OrderItemForm
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

# Create your views here.

class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orserapp:orders_list')

    OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
    basket_items = Basket.objects.filter(self.request.user)

    if len(basket_items):
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
        formset=OrderFormSet
        for num, form in enumerate(formset.forms):
            form.initial['product'] = basket_items['num'].product
            form.initial['quantity'] = basket_items['num'].quantity
            basket_items.delete()
    else:
        formset = OrderFormSet

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        data['orderitems'] = self.formset
        if self.request.POST:
            formset = self.OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.get_items(self.request.user)
            if len(basket_items):
                for num, form in enumerate(self.formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price

        return data

    form.instance.user = self.request.user
    context = self.get_context_data()
    orderitems = context['orderitems']

    def form_valid(self, form):

        with transaction.atomic():
            form.instance.user = self.request.user
            if self.orderitems.is_valid():
                self.orderitems.instance = self.object
                self.orderitems.seve()
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsCreate, self).form_valid(form)
class OrderUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orserapp:orders_list')

    OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['orderitems'] = self.OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = self.OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
            data['orderitems'] = formset
        return data

    with transaction.atomic():
        self.object = object.save()
        if self.orderitems.is_valid:
            self.orderitems.instance = self.object

    @receiver(pre_save, sender=OrderItem)
    @receiver(pre_save, sender=Basket)
    def product_quantity_update_save(sender, update_fields, instance, **kwargs):
        if update_fields is 'quantity' or 'product':
            if instance.pk:
                instance.product.quantity -= instance.quantity - \
                                             sender.get_item(instance.pk).quantity
            else:
                instance.product.quantity -= instance.quantity
            instance.product.save()

class OrderDelete(DeleteView):
    model = Order
    fields = []
    success_url = reverse_lazy('orserapp:orders_list')

    @receiver(pre_delete, sender=OrderItem)
    @receiver(pre_delete, sender=Basket)
    def product_quantity_update_delete(sender, instance, **kwargs):
        instance.product.quantity += instance.quantity
        instance.product.save()



class OrderRead(DetailView):
   model = Order

   def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        context['title'] = 'заказ/просмотр'
        return context

def order_forming_complete(request, pk):
   order = get_object_or_404(Order, pk=pk)
   order.status = Order.SENT_TO_PROCEED
   order.save()

   return HttpResponseRedirect(reverse('ordersapp:orders_list'))