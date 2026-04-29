from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer
from rest_framework.throttling import  UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from users.permissions import IsAdmin, IsRegularUser
from drf_spectacular.utils import extend_schema

@extend_schema(request=None, responses={200: CategorySerializer(many=True)}, tags=['Categories'])
@api_view(['GET'])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
@permission_classes([AllowAny])
def category_list(request): 
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

