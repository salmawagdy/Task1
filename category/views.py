from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer
from rest_framework.throttling import  UserRateThrottle, AnonRateThrottle

@api_view(['GET'])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def category_list(request): 
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

