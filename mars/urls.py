from django.urls import path

from .views import note, notebook, tag

urlpatterns = [
    path('notebooks/', notebook.index, name='Notebooks'),
    path('notebooks/<str:notebook_key>/', notebook.entry, name='Notebook'),
    path('notes/', note.index, name="Notes"),
    path('notes/<str:note_key>', note.entry, name="Note"),
    path('tags/', tag.index, name="Tags"),
    path('tags/<str:tag_key>', tag.entry, name="Tag")
]
