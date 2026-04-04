from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework.throttling import  UserRateThrottle, AnonRateThrottle


@api_view(['GET'])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def product_list(request):
    search = request.query_params.get('search')
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')

    products = Product.objects.all()

    
    if search:
        products = products.filter(name__icontains=search)

    
    if min_price:
        products = products.filter(price__gte=min_price)

    
    if max_price:
        products = products.filter(price__lte=max_price)

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def active_products(request):
    products = Product.objects.filter(is_active=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)