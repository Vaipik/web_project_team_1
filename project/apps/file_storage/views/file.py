from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView, DetailView, UpdateView

from ..forms import FileForm, EditFileForm
from ..models import File
from .. import services


class FileListView(LoginRequiredMixin, ListView):
    template_name = "file_storage/pages/file_list.html"
    context_object_name = "files"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs.update(
            title=f"{self.owner.username} files"
        )
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.owner = self.request.user
        return services.get_user_files(owner=self.owner)


class FileDetailView(LoginRequiredMixin, DetailView):
    template_name = "file_storage/pages/file_view.html"
    pk_url_kwarg = "file_uuid"
    extra_context = {"title": "Detailed file description"}
    context_object_name = "file"

    def get_object(self, queryset=None):
        print(self.kwargs["file_uuid"])
        return services.get_file(self.kwargs["file_uuid"])


class UploadFileView(LoginRequiredMixin, FormView):
    template_name = 'file_storage/pages/upload_page.html'
    form_class = FileForm
    success_url = reverse_lazy("file_storage:file_list")
    extra_context = {"title": "Uploading file"}

    def form_valid(self, form):
        data = form.cleaned_data
        services.upload_file(
            **data,
            owner=self.request.user
        )
        return super().form_valid(form)


class DeleteFileView(LoginRequiredMixin, View):

    def post(self, request, file_uuid):
        file = services.get_file(file_uuid)
        file.delete()
        return JsonResponse(
            data={
                "message": "File deleted",
                "status": "204",
                "url": redirect("file_storage:file_list").url
            },
            status=200
        )


class EditFileDescriptionView(LoginRequiredMixin, UpdateView):
    form_class = EditFileForm
    model = File
    template_name = "file_storage/pages/editing_file.html"
    extra_context = {"title": "Editing file"}
    pk_url_kwarg = "file_uuid"
    success_url = reverse_lazy("file_storage:file_list")

    def form_valid(self, form):
        self.object.description = form.cleaned_data["description"]
        self.object.save()
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return services.get_file(self.kwargs["file_uuid"])
