from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .serializers import ProductSerializer, OrderSerializer
from shop.models import Products, Order
from django.core.paginator import Paginator
# Create your views here.


def features(request):
    return render(request, 'shop/features.html')


def disabled(request):
    return render(request, 'shop/disabled.html')


def index(request):
    products_object = Products.objects.all()

    # Search code
    items_name = request.GET.get('items_name')
    if items_name != '' and items_name is not None:
        products_object = products_object.filter(
            title__icontains=items_name)
    # Paginaor code
    paginator = Paginator(products_object, 4)
    page = request.GET.get('page')
    products_object = paginator.get_page(page)
    return render(
        request, 'shop/index.html',
        {'products_object': products_object}
    )


def details(request, id):
    products_object = Products.objects.get(id=id)
    return render(
        request, 'shop/details.html',
        {'products_object': products_object}
    )


def product_detail(request, id):
    product = get_object_or_404(Products, id=id)
    return render(
        request, 'shop/product_detail.html',
        {'product': product}
    )


def checkout(request):

    if request.method == "POST":
        items = request.POST.get('items', "")
        name = request.POST.get('name', "")
        email = request.POST.get('email', "")
        address = request.POST.get('address', "")
        city = request.POST.get('city', "")
        state = request.POST.get('state', "")
        zipcode = request.POST.get('zipcode', "")
        total = request.POST.get('total', "")

        order = Order(
            items=items, name=name, email=email, address=address,
            city=city, state=state, zipcode=zipcode, total=total
        )
        order.save()

    return render(request, 'shop/checkout.html')


class ProductViewset(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
