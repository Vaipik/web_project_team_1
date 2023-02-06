from django.urls import path, re_path

from . import views

app_name = "file_storage"

urlpatterns = [
    path("", views.FileListView.as_view(), name="file_list"),
    re_path(r"upload/$", views.UploadFileView.as_view(), name="upload_file"),
    path("<uuid:file_uuid>/", views.FileDetailView.as_view(), name="show_file"),
    path("delete/<uuid:file_uuid>/", views.DeleteFileView.as_view(), name="delete_file"),
    path("editing/<uuid:file_uuid>/", views.EditFileDescriptionView.as_view(), name="edit_file"),
    path("<slug:category_url>/", views.FileByCategoryListView.as_view(), name="show_category_files")
]
