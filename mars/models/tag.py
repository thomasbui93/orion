from django.db import models
from django.contrib.auth.models import User
import uuid


class Tag(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField('created date', auto_now_add=True)
    updated_date = models.DateTimeField('updated date', auto_now=True)

    def __str__(self):
        return self.title
