from django.contrib import admin

# Register your models here.
from .models.note import Note
from .models.tag import Tag
from .models.notebook import Notebook

admin.site.register(Note)
admin.site.register(Tag)
admin.site.register(Notebook)
