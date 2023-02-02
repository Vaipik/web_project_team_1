from django.urls import path, re_path

from . import views

app_name = "file_storage"

urlpatterns = [
    path("", views.ShowFilesView.as_view(), name="file_list"),
    re_path(r"upload/$", views.UploadFileView.as_view(), name="upload_file"),
]
