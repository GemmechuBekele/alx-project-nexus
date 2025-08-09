"""
URL configuration for ecomsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers
from shop import views
from shop.views import (
    ProductViewSet, OrderViewset,
    API, DetailsAPI, IndexAPI,
    CheckoutAPI, CategoryViewSet
)
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Shop API",
        default_version='v1',
        description="Shop API with products, categories, orders",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="gemmechu.bekele.berga@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('products', ProductViewSet, basename='products')
router.register('orders', OrderViewset, basename='orders')

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api-swagger/', API.as_view(), name='api-swagger'),
    path(
        'swagger/', schema_view.with_ui('swagger',
                                        cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('features/', views.features, name='features'),
    path('disabled/', views.disabled, name='disabled'),
    path('checkout/', views.checkout, name='checkout'),
    path('<int:id>/', views.product_detail, name='product_detail')
]
urlpatterns += [
    path('api/checkout/', CheckoutAPI.as_view(), name='api-checkout'),
    path('api/details/', DetailsAPI.as_view(), name='api-details'),
    path('api/index/', IndexAPI.as_view(), name='api-index'),

]
