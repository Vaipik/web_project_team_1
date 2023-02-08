from django.urls import path, re_path

from . import views

app_name = "notes"

urlpatterns = [
    path("", views.main, name="note"),
    path('tag/', views.tag, name="tag"),
    path('note/', views.note, name="note"),
    path('detail/<int:note_id>', views.detail, name="detail"),
    path('done/<int:note_id>', views.set_done, name="set_done"),
    path('delete/<int:note_id>', views.delete_note, name="delete"),
]

# path("delete/<uuid:file_uuid>/", views.DeleteFileView.as_view(), name="delete_file"),
# path("editing/<uuid:file_uuid>/", views.EditFileDescriptionView.as_view(), name="edit_file"),
# path("<uuid:file_uuid>/", views.FileDetailView.as_view(), name="show_file"),
# re_path(r"upload/$", views.UploadFileView.as_view(), name="upload_file"),
# path("<slug:category_url>/", views.FileByCategoryListView.as_view(), name="show_category_files"),
# path("", views.FileListView.as_view(), name="file_list"),
