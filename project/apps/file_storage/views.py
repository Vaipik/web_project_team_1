from django.views.generic import FormView, ListView, DetailView
from django.urls import reverse

from .forms import FileForm
from . import services


class ShowFilesView(ListView):
    pass


class ShowSingleFileView(DetailView):
    pass


class UploadFileView(FormView):
    template_name = 'file_storage/pages/upload_page.html'
    form_class = FileForm
    success_url = "/files/"

    def form_valid(self, form):
        data = form.cleaned_data
        services.upload_file(
            **data,
            owner=self.request.user
        )
        return super().form_valid(form)
