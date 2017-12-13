from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from .models import Notebook, Note, Tag


class NotebookSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(default=CurrentUserDefault(), read_only=True)

    class Meta:
        model = Notebook
        fields = ('title', 'key', 'created_date', 'updated_date', 'user')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('title', 'key', 'created_date', 'updated_date')

    def save(self):
        user = CurrentUserDefault()


class NoteSerializer(serializers.ModelSerializer):
    notebook = NotebookSerializer(many=False)
    tags = TagSerializer(many=True)

    class Meta:
        model = Note
        fields = ('title', 'key', 'content', 'tags', 'notebook', 'created_date', 'updated_date')

    def save(self):
        user = CurrentUserDefault()


class NoteThumbSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ('title', 'key', 'excerpt', 'created_date', 'updated_date')

    def save(self):
        user = CurrentUserDefault()
