from django.views.generic import FormView, ListView, DetailView
from django.urls import reverse

from .. import services


class FileByCategoryListView(ListView):
    template_name = "file_storage/pages/category_file_list.html"
    context_object_name = "files"
    paginate_by = 5
    slug_url_kwarg = "category_url"

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs.update(
            title=f"{self.owner.username} files"
        )
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.owner = self.request.user
        return services.get_user_category_files(
            user=self.owner,
            category_url=self.kwargs["category_url"]
        )

