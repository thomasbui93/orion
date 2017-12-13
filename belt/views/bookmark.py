from belt.models import Bookmark, Folder
from belt.serializers import BookmarkSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required


@login_required()
@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'GET':
        current_user = request.user
        folders = Bookmark.objects.filter(user=current_user.id)
        serializer = BookmarkSerializer(folders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BookmarkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required()
@api_view(['GET', 'PUT', 'DELETE'])
def entry(request, bookmark_id):
    try:
        current_user = request.user
        bookmark = Bookmark.objects.get(pk=bookmark_id, user=current_user.id)
    except Bookmark.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = BookmarkSerializer(bookmark)
        return Response(serializer.data)

    elif request.method == 'PUT':

        serializer = BookmarkSerializer(bookmark, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':

        bookmark.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@login_required()
@api_view(['GET'])
def folder_entry(request, folder_id):
    try:
        Folder.objects.get(pk=folder_id)
    except Folder.DoesNotExist:
        return Response(status=404)

    bookmarks = Bookmark.objects.filter(folder=folder_id)
    serializer = BookmarkSerializer(bookmarks, many=True)
    return Response(serializer.data)
