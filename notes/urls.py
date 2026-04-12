from django.urls import path
from .views import home, edit_note, delete_note, increment_read_count

urlpatterns = [
    path('', home, name='home'),
    path('edit/<int:note_id>/', edit_note, name='edit_note'),
    path('delete/<int:note_id>/', delete_note, name='delete_note'),
    path('increment-read/<int:note_id>/', increment_read_count, name='increment_read_count'),
]
