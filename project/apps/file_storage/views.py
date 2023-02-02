from django.views.generic import FormView, ListView, DetailView
from django.urls import reverse

from .forms import FileForm
from . import services


class ShowFilesView(ListView):
    template_name = "file_storage/pages/file_list.html"
    context_object_name = "files"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs.update(
            title=f"{self.owner.username} files"
        )
        context = super().get_context_data(**kwargs)
        print(context)
        return context

    def get_queryset(self):
        self.owner = self.request.user
        return services.get_user_files(owner=self.owner)


class ShowSingleFileView(DetailView):
    pass


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
