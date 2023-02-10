from django.urls import path, re_path

from . import views

app_name = "notes"

urlpatterns = [
    path('delete/<slug:note_id>', views.delete_note, name="delete"),
    path('done/<slug:note_id>', views.set_done, name="set_done"),
    path('detail/<slug:note_id>', views.detail, name="detail"),
    path('filter_note/', views.filter_notes, name="filter_note"),
    path('add_note/', views.add_note, name="add_note"),
    path('add_tag/', views.add_tag, name="add_tag"),
    path("", views.main, name="main"),
]

