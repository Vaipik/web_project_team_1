from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from utils.pagination import PaginationMixin
from .. import services
from ..mixins import UserCategoryMixin


class FileByCategoryListView(LoginRequiredMixin, PaginationMixin, UserCategoryMixin, ListView):
    template_name = "file_storage/pages/category_file_list.html"
    context_object_name = "files"
    paginate_by = 5
    slug_url_kwarg = "category_url"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(
            **kwargs,
            title=f"{self.owner.username} files",
            category_url=self.kwargs["category_url"]
        )
        context.update(
            **self.get_pages(page_obj=context["page_obj"]),
            **self.get_user_categories()
        )
        return context

    def get_queryset(self):
        self.owner = self.request.user
        return services.get_user_category_files(
            user=self.owner,
            category_url=self.kwargs["category_url"]
        )

