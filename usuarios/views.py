from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.password_validation import validate_password
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, UserRegistrationWithJWTSerializer

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """ Criar um novo usuário """

    data = request.data

    try:
        # validar senha
        validate_password(data.get('password'))

        # validar se o usuário já existe
        if User.objects.filter(username=data.get('username')).exists():
            return Response({'error': 'Username já existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=data.get('email')).exists():
            return Response({'error': 'Email já existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(telefone=data.get('telefone')).exists():
            return Response({'error': 'Telefone já existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        # criar o usuário
        user = User.objects.create_user(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            fist_name=data.get('first_name'),
            last_name=data.get('last_name'),
            telefone=data.get('telefone'),
            is_staff=False,
            is_superuser=False,
        )

        return Response({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'telefone': user.telefone,
        }, status=status.HTTP_201_CREATED)
    
    except ValidationError as e:
        return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

class CustomTokenObtainPairView(TokenObtainPairView):
    """ View personalizada para login com JWT """
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user_with_jwt(request):
    """ Criar um novo usuário e retornar os tokens JWT """

    serializer = UserRegistrationWithJWTSerializer(data=request.data)

    if serializer.is_valid():
        result = serializer.save()
        return Response(result, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_detail(request):
    """ Retorna os dados do usuário authenticado """

    user = request.user({
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
        'telefone': user.telefone,
    })