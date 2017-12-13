from django.db import models
from django.contrib.auth.models import User
from .tag import Tag
from .notebook import Notebook
import uuid


class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    excerpt = models.TextField()
    key = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    created_date = models.DateTimeField('created date', auto_now_add=True)
    updated_date = models.DateTimeField('updated date', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']
