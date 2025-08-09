from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer
from .pagination import CustomPageNumberPagination
from .models import Category, Product, Order
from django.core.paginator import Paginator
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class API(APIView):
    @swagger_auto_schema(
        operation_summary="Example API endpoint",
        operation_description="This is an example generic API endpoint with Swagger documentation.",
        responses={200: "Success", 400: "Bad Request"}
    )
    def get(self, request, *args, **kwargs):
        return Response({"message": "Hello from API"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a message",
        operation_description="Accepts JSON with a 'text' field and returns it back.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'text': openapi.Schema(type=openapi.TYPE_STRING, description="Message text")
            },
            required=['text']
        ),
        responses={201: openapi.Response('Created')}
    )
    def post(self, request, *args, **kwargs):
        text = request.data.get("text", "")
        return Response({"received": text}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Update a message",
        operation_description="Replaces the existing message with a new one.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'text': openapi.Schema(type=openapi.TYPE_STRING, description="Updated message text")
            },
            required=['text']
        ),
        responses={200: openapi.Response('Updated')}
    )
    def put(self, request, *args, **kwargs):
        text = request.data.get("text", "")
        return Response({"updated": text}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Partially update a message",
        operation_description="Partially updates the message with given fields.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'text': openapi.Schema(type=openapi.TYPE_STRING, description="Partial updated text")
            }
        ),
        responses={200: openapi.Response('Partially Updated')}
    )
    def patch(self, request, *args, **kwargs):
        text = request.data.get("text", "")
        return Response({"partially_updated": text}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Delete a message",
        operation_description="Deletes the resource (simulation).",
        responses={204: 'No Content'}
    )
    def delete(self, request, *args, **kwargs):
        return Response(status=status.HTTP_204_NO_CONTENT)


class IndexAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Home Page",
        operation_description="Returns data for the home page.",
        responses={200: "Success"}
    )
    def get(self, request, *args, **kwargs):
        data = {"message": "Home page data or summary"}
        return Response(data)


class DetailsAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Details Page",
        operation_description="Returns info or data related to the Details page.",
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_QUERY,
                description="Product ID",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={200: "Success", 404: "Not Found"}
    )
    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('id')
        if not product_id:
            return Response({"error": "Product id required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CheckoutAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Checkout Page",
        operation_description="Returns info or data related to the checkout page.",
        responses={200: "Success"}
    )
    def get(self, request, *args, **kwargs):
        # Example: return simple JSON or some data you want to expose via API
        data = {"message": "Checkout page data or info"}
        return Response(data)


def features(request):
    return render(request, 'shop/features.html')


def disabled(request):
    return render(request, 'shop/disabled.html')


def index(request):
    products_object = Product.objects.all()

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
    products_object = Product.objects.get(id=id)
    return render(
        request, 'shop/details.html',
        {'products_object': products_object}
    )


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(
        request, 'shop/product_detail.html',
        {'product': product}
    )


def checkout(request):

    if request.method == "POST":
        items_str = request.POST.get('items', "")
        name = request.POST.get('name', "")
        email = request.POST.get('email', "")
        address = request.POST.get('address', "")
        city = request.POST.get('city', "")
        state = request.POST.get('state', "")
        zipcode = request.POST.get('zipcode', "")
        total = request.POST.get('total', "")

        items_ids = []
        if items_str:
            items_ids = [int(i) for i in items_str.split(',') if i.isdigit()]

        order = Order(
            name=name, email=email, address=address,
            city=city, state=state, zipcode=zipcode, total=total
        )
        order.save()

        products = Product.objects.filter(id__in=items_ids)
        order.items.set(products)

    return render(request, 'shop/checkout.html')


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class ProductViewSet(viewsets.ModelViewSet):
    """
    list:
    Return a list of all products.

    retrieve:
    Return details of a specific product.

    create:
    Create a new product.

    update:
    Update a product.

    partial_update:
    Partially update a product.

    destroy:
    Delete a product.
    """
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CustomPageNumberPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['category__id', 'category__name']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at', 'title']
    ordering = ['-created_at']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class OrderViewset(viewsets.ModelViewSet):
    """
    list:
    Return a list of all orders.

    retrieve:
    Return details of a specific order.

    create:
    Create a new order.

    update:
    Update an order.

    partial_update:
    Partially update an order.

    destroy:
    Delete an order.
    """
    queryset = Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
