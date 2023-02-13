from django.urls import path

from . import views

app_name = "notes"

urlpatterns = [
    path('delete/<slug:note_id>', views.delete_note, name="delete"),
    path('undone/<slug:note_id>', views.set_undone, name="set_undone"),
    path('done/<slug:note_id>', views.set_done, name="set_done"),
    path('detail/<slug:note_id>', views.detail, name="detail"),

    path('edit/<slug:note_id>', views.edit_note, name="edit"),
    path('save/<slug:note_id>', views.save_note, name="save_note"),
    path('delete_tag/', views.delete_tag, name="delete_tag"),
    path('add_note/', views.add_note, name="add_note"),
    path('tags/', views.add_tag, name="tags"),

    path("", views.main, name="main"),
]

