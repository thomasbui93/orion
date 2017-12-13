from django.urls import path

from .views import folder, bookmark

urlpatterns = [
    path('', folder.index, name='Folders'),
    path('<int:folder_id>/', folder.entry, name='Folder'),
    path('bookmark/', bookmark.index, name="Bookmarks"),
    path('bookmarks/<int:folder_id>', bookmark.folder_entry, name="Bookmarks"),
    path('bookmark/<int:bookmark_id>', bookmark.entry, name="Bookmark")
]
