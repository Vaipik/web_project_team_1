from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, DetailView, UpdateView, DeleteView

from utils.pagination import PaginationMixin
from ..forms import FileForm, EditFileForm
from ..models import File
from .. import services
from ..mixins import UserCategoryMixin


class FileListView(LoginRequiredMixin, PaginationMixin, UserCategoryMixin, ListView):
    template_name = "file_storage/pages/show_files.html"
    context_object_name = "files"
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs, title=f"{self.owner.username} files")
        context.update(
            **self.get_pages(
                page_obj=context["page_obj"],
            ),
            **self.get_user_categories()

        )
        return context

    def get_queryset(self):
        self.owner = self.request.user
        return services.get_user_files(owner=self.owner)


class FileDetailView(LoginRequiredMixin, UserCategoryMixin, DetailView):
    template_name = "file_storage/pages/file_view.html"
    pk_url_kwarg = "file_uuid"
    extra_context = {"title": "File data"}
    model = File

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            **self.get_user_categories()
        )
        return context


class UploadFileView(LoginRequiredMixin, UserCategoryMixin, FormView):
    template_name = 'file_storage/pages/upload_page.html'
    form_class = FileForm
    success_url = reverse_lazy("file_storage:file_list")
    extra_context = {"title": "Uploading file"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            **self.get_user_categories()
        )
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        services.upload_file(
            **data,
            owner=self.request.user
        )
        return super().form_valid(form)


class DeleteFileView(LoginRequiredMixin, DeleteView):
    pk_url_kwarg = "file_uuid"
    model = File
    success_url = reverse_lazy("file_storage:file_list")


class EditFileDescriptionView(LoginRequiredMixin, UserCategoryMixin, UpdateView):
    template_name = "file_storage/pages/editing_file.html"
    pk_url_kwarg = "file_uuid"
    form_class = EditFileForm
    model = File
    extra_context = {"title": "Editing file"}
    success_url = reverse_lazy("file_storage:file_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            **self.get_user_categories()
        )
        return context
