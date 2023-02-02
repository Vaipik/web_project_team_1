from django.urls import path, re_path

from . import views

app_name = "file_storage"

urlpatterns = [
    re_path(r"upload/$", views.UploadFileView.as_view(), name="upload_file"),
]
