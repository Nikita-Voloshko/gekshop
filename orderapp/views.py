import self as self
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction

from django.forms import inlineformset_factory
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from basket.models import Basket
from orderapp.models import Order, OrderItem
from orderapp.forms import OrderItemForm

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
    basket_items = Basket.get_items(self.request.user)
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
class OrderUpdateVie(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orserapp:orders_list')

    OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

    if self.request.POST:
        data['orderformset'] = OrderFormSet(self.request.POST, instance=self.object)
    else:
        data['orderformset'] = OrderFormSet(instance=self.object)

    with transaction.atomic():
        self.object = object.save()
        if self.orderitems.is_valid:
            self.orderitems.instance = self.object

class OrderDelete(DeleteView):
    model = Order
    fields = []
    success_url = reverse_lazy('orserapp:orders_list')




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