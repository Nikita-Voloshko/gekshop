import orderapp.views as ordersapp
from django.urls import path

app_name="ordersapp"

urlpatterns = [
   path('orders_list/', ordersapp.OrderList.as_view(), name='orders_list'),
   path('order_forming_complete/', ordersapp.order_forming_complete, name='order_forming_complete'),
   path('order_create/', ordersapp.OrderItemsCreate.as_view(), name='order_create'),
   path('order_read', ordersapp.OrderRead.as_view(), name='order_read'),
   path('order_update/', ordersapp.OrderItemsUpdate.as_view(), name='order_update'),
   path('order_delete/', ordersapp.OrderDelete.as_view(), name='order_delete'),
]