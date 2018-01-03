from mars.models import Note, Notebook, Tag
from django.http import JsonResponse
from mars.serializers import TagSerializer, TagThumbSerializer, NoteThumbSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes(IsAuthenticated)
@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'GET':
        current_user = request.user
        tags = Tag.objects.filter(user=current_user.id)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes(IsAuthenticated)
@api_view(['GET'])
def search(request):

    tags = Tag.objects.filter(user=request.user.id, title__contains=request.GET.get('query', default=''))
    paginator = Paginator(tags, 5)
    page = request.GET.get('page', 1)

    try:
        tag_list = paginator.page(page)
    except PageNotAnInteger:
        tag_list = paginator.page(1)
    except EmptyPage:
        tag_list = paginator.page(paginator.num_pages)

    serializer = TagThumbSerializer(tag_list, many=True, context={'request': request})
    return Response(serializer.data)


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes(IsAuthenticated)
@api_view(['GET', 'POST'])
def entry(request, tag_key):
    try:
        current_user = request.user
        tag = Tag.objects.get(key=tag_key, user=current_user.id)
    except Notebook.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = TagSerializer(tag)

        notes_list = Note.objects.filter(tags__in=[tag.id], user=current_user.id)
        paginator = Paginator(notes_list, 25)
        page = request.GET.get('page')

        try:
            notes = paginator.page(page)
        except PageNotAnInteger:
            notes = paginator.page(1)
        except EmptyPage:
            notes = paginator.page(paginator.num_pages)

        note_serializer = NoteThumbSerializer(notes, many=True)

        return JsonResponse({
            'tag': serializer.data,
            'notes': note_serializer.data
        })

    elif request.method == 'PUT':

        serializer = TagSerializer(tag, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':

        tag.delete()

        return JsonResponse({
            'status': True
        })