from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from .models import Folder, Bookmark


class FolderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = ('id', 'folder_name', 'created_date', 'updated_date')

    def save(self):
        user = CurrentUserDefault()


class BookmarkSerializer(serializers.ModelSerializer):
    folder = serializers.StringRelatedField(many=False)

    class Meta:
        model = Bookmark
        fields = ('id', 'name', 'note', 'url', 'created_date', 'updated_date', 'folder')

    def save(self):
        user = CurrentUserDefault()
