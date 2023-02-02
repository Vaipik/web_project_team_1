from django.views.generic import FormView, ListView, DetailView
from django.urls import reverse

from ..forms import FileForm
from .. import services


class FileListView(ListView):
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


class FileDetailView(DetailView):
    template_name = "file_storage/pages/file_view.html"
    pk_url_kwarg = "file_uuid"
    extra_context = {"title": "Detailed file description"}
    context_object_name = "file"

    def get_object(self, queryset=None):
        print(self.kwargs["file_uuid"])
        return services.get_file(self.kwargs["file_uuid"])


class UploadFileView(FormView):
    template_name = 'file_storage/pages/upload_page.html'
    form_class = FileForm
    success_url = "/files/"
    extra_context = {"title": "Uploading file"}

    def form_valid(self, form):
        data = form.cleaned_data
        services.upload_file(
            **data,
            owner=self.request.user
        )
        return super().form_valid(form)
