from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework.throttling import  UserRateThrottle, AnonRateThrottle
from .paginations import CustomPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from users.permissions import IsAdmin, IsRegularUser
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
import time 
from drf_spectacular.utils import extend_schema


@extend_schema(request=None, responses={200: ProductSerializer(many=True)}, tags=['Products']) 
@api_view(['GET'])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
@permission_classes([AllowAny])
@cache_page(60 * 15)
@vary_on_headers('User-Agent')
def product_list(request):

    search = request.query_params.get('search')
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')

    products = Product.objects.select_related('category').all()

    time.sleep(3)

    if search:
        products = products.filter(name__icontains=search)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)


    products = list(products)

    paginator = CustomPagination()
    paginated_products = paginator.paginate_queryset(products, request)

    serializer = ProductSerializer(paginated_products, many=True)

    return paginator.get_paginated_response(serializer.data)

@extend_schema(request=None, responses={200: ProductSerializer(many=True)}, tags=['Products'])
@api_view(['GET'])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
@permission_classes([IsAuthenticated])
def active_products(request):
    products = Product.objects.filter(is_active=True)
    paginator = CustomPagination()
    paginated_products = paginator.paginate_queryset(products, request)
    serializer = ProductSerializer(paginated_products, many=True)
    return paginator.get_paginated_response(serializer.data)


@extend_schema(request=ProductSerializer, responses={201: ProductSerializer}, tags=['Products'])
@api_view(['POST'])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
@permission_classes([IsAuthenticated, IsAdmin])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)