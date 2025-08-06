from django.shortcuts import render
from shop.models import Products, Order
from django.core.paginator import Paginator
# Create your views here.


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
    return render(request, 'shop/index.html', {'products_object': products_object})


def details(request, id):
    products_object = Products.objects.get(pk=id)
    return render(request, 'shop/details.html', {'products_object': products_object})


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

        order = Order(items=items, name=name, email=email, address=address,
                      city=city, state=state, zipcode=zipcode, total=total)
        order.save()

    return render(request, 'shop/checkout.html')
