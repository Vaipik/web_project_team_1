from .models import FileCategory


class UserCategoryMixin:

    def get_user_categories(self, **kwargs):
        context = kwargs
        context["categories"] = FileCategory.objects. \
            prefetch_related("category"). \
            filter(category__owner=self.request.user).\
            distinct()

        return context
