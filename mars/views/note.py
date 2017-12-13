from mars.models import Note
from mars.serializers import NoteSerializer, NoteThumbSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required()
@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'GET':
        current_user = request.user
        notes_list = Note.objects.filter(user=current_user.id)
        paginator = Paginator(notes_list, 25)
        page = request.GET.get('page')

        try:
            notes = paginator.page(page)
        except PageNotAnInteger:
            notes = paginator.page(1)
        except EmptyPage:
            notes = paginator.page(paginator.num_pages)

        serializer = NoteThumbSerializer(notes, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required()
@api_view(['GET', 'PUT', 'DELETE'])
def entry(request, note_key):
    try:
        current_user = request.user
        note = Note.objects.get(key=note_key, user=current_user.id)
    except Note.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    elif request.method == 'PUT':

        serializer = NoteSerializer(note, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':

        note.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)