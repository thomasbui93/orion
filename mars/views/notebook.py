from mars.models import Note, Notebook
from django.http import JsonResponse
from mars.serializers import NotebookSerializer, NoteThumbSerializer, NotebookThumbSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes(IsAuthenticated)
@api_view(['GET', 'POST'])
def index(request):

    if request.method == 'GET':
        current_user = request.user
        notebooks = Notebook.objects.filter(user=current_user.id)
        serializer = NotebookSerializer(notebooks, many=True,  context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = NotebookSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes(IsAuthenticated)
@api_view(['GET'])
def search(request):

    notebooks = Notebook.objects.filter(user=request.user.id, title__contains=request.GET.get('query', default=''))
    paginator = Paginator(notebooks, 5)
    page = request.GET.get('page', 1)

    try:
        notebook_list = paginator.page(page)
    except PageNotAnInteger:
        notebook_list = paginator.page(1)
    except EmptyPage:
        notebook_list = paginator.page(paginator.num_pages)

    serializer = NotebookThumbSerializer(notebook_list, many=True, context={'request': request})
    return Response(serializer.data)


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes(IsAuthenticated)
@api_view(['GET', 'PUT', 'DELETE'])
def entry(request, notebook_key):
    try:
        current_user = request.user
        notebook = Notebook.objects.get(key=notebook_key, user=current_user.id)

    except Notebook.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = NotebookSerializer(notebook, context={'request': request})

        notes_list = Note.objects.filter(notebook=notebook, user=current_user.id)
        paginator = Paginator(notes_list, 5)
        page = request.GET.get('page')

        try:
            notes = paginator.page(page)
        except PageNotAnInteger:
            notes = paginator.page(1)
        except EmptyPage:
            notes = paginator.page(paginator.num_pages)

        note_serializer = NoteThumbSerializer(notes, many=True, context={'request': request})

        return JsonResponse({
            'notebook': serializer.data,
            'notes': note_serializer.data,
            'pagination': {
                'count': paginator.count,
                'pages': paginator.num_pages
            }
        })

    elif request.method == 'PUT':
        serializer = NotebookSerializer(notebook, data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':

        notebook.delete()

        return JsonResponse({
            'status': True
        })
