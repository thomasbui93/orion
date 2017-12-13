from django.db import models
from django.contrib.auth.models import User


class Folder(models.Model):
    folder_name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField('created date', auto_now_add=True)
    updated_date = models.DateTimeField('updated date', auto_now=True)

    def __str__(self):
        return self.folder_name


class Bookmark(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    note = models.TextField()
    url = models.URLField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField('created date', auto_now_add=True)
    updated_date = models.DateTimeField('updated date', auto_now=True)

    def __str__(self):
        return self.name
