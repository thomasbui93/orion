from belt.models import Folder
from belt.serializers import FolderSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required


@login_required()
@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'GET':
        current_user = request.user
        folders = Folder.objects.filter(user=current_user.id)
        serializer = FolderSerializer(folders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = FolderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required()
@api_view(['GET', 'PUT', 'DELETE'])
def entry(request, folder_id):
    try:
        current_user = request.user
        folder = Folder.objects.get(pk=folder_id, user=current_user.id)
    except Folder.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = FolderSerializer(folder)
        return Response(serializer.data)

    elif request.method == 'PUT':

        serializer = FolderSerializer(folder, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':

        folder.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


