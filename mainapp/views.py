from django.shortcuts import render
from mainapp.models import Product, ProductCategory
# Create your views here.
def index(request):
    return render(request, 'mainapp/index.html')


def products(request, category_id=None):
    context = {
        'products': Product.objects.filter(category_id=category_id) if category_id else Product.objects.all(),
        'categories':  ProductCategory.objects.all()
    }
    return render(request, 'mainapp/products.html', context)
