from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from .models import Notebook, Note, Tag


class NotebookSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(default=CurrentUserDefault(), read_only=True)

    class Meta:
        model = Notebook
        fields = ('title', 'key', 'created_date', 'updated_date', 'user')


class TagSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(default=CurrentUserDefault(), read_only=True)

    class Meta:
        model = Tag
        fields = ('title', 'key', 'created_date', 'updated_date', 'user')


class NoteSerializer(serializers.ModelSerializer):
    notebook = NotebookSerializer(many=False)
    tags = TagSerializer(many=True)
    user = serializers.StringRelatedField(default=CurrentUserDefault(), read_only=True)

    class Meta:
        model = Note
        fields = ('title', 'key', 'content', 'tags', 'notebook', 'created_date', 'updated_date', 'user')

    def to_internal_value(self, data):
        try:
            if 'notebook' in data:
                current_user = self.context['request'].user
                notebook = Notebook.objects.get(key=data['notebook'], user=current_user.id)
                data['notebook'] = notebook
            return data
        except Notebook.DoesNotExist:
            raise serializers.ValidationError("Notebook is not found.")

    def create(self, validated_data):
        current_user = self.context['request'].user
        note = Note.objects.create(user=current_user, **validated_data)
        return note


class NoteThumbSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(default=CurrentUserDefault(), read_only=True)

    class Meta:
        model = Note
        fields = ('title', 'key', 'excerpt', 'created_date', 'updated_date', 'user')

