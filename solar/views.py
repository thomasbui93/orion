from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
import json


@api_view(['GET'])
def get_me(request):
    current_user = request.user
    serializer = UserSerializer(current_user)
    return Response(serializer.data)


@csrf_exempt
def login_attempt(request):
    body = json.loads(request.body.decode('utf-8'))
    username = body['username'] if 'username' in body else None
    password = body['password'] if 'password' in body else None
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({"token": token.key}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'message': 'Failed to authenticate.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
def logout_attempt(request):
    try:
        logout(request)
        return JsonResponse({'message': 'Authenticated successfully.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)
