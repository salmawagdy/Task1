# user/views.py
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, UserSerializer
from .permissions import IsAdmin, IsRegularUser
from rest_framework.permissions import IsAdminUser
from django.db import transaction
from .tasks import send_welcome_email


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        with transaction.atomic():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)

        # 🚀 Celery background task
        send_welcome_email.delay(user.email)

        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)

    return Response({
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if not user:
        return Response(
            {"error": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        "user": UserSerializer(user).data,
        "token": token.key
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({"message": "Logged out successfully."})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)