from django.shortcuts import render

from django.template.loader import render_to_string
from django.http import JsonResponse


from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basket.models import Basket
from mainapp.models import Product
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def basket_add(request, product_id=None):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user)

    if baskets.exists():
        basket = Basket(user=request.user, product=product)
        basket.quantity = + 1
        basket.save

        print(basket)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        basket = baskets.first
        basket.quantity = + 1
        basket.save
        print(basket)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_remove(request, id):
    basket = Basket.objects.get(id=id)
    basket.delete()

@login_required
def basket_edit(request, id, quntity):
    if request.is_ajax():
        quntity = int(quntity)
        basket = Basket.objects.get(id=int(id))
        if quntity > 0:
            quntity = quntity + 1
            basket.save()
        else:
            basket.delete()
        basket = Basket.objects.filter(user=request.user)
        context = {basket: basket, }

        result = render_to_string('basket/basket.html', context)
        JsonResponse({'result': result})
