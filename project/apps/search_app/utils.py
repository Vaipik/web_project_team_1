from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect


def get_filter_query_conditions(fields: list, query_string: str):
    filter_conditions = Q()
    query_list = query_string.split()

    if query_list:
        for query in query_list:
            for field in fields:
                filter_conditions = (
                    filter_conditions | Q(**{f"{field}__icontains": query})
                )

    return filter_conditions


class SearchAppMixin:
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        query_string = self.request.GET.get("search", None)
        if query_string:
            query_list = query_string.split()
            context.update({"query": query_list})
        return context

    def get_queryset(self):
        query = self.request.GET.get("search", None)
        if query is None:
            messages.error(self.request, "Please enter some keyword to search")
            redirect(self.request.META.get("HTTP_REFERER"))

        filter_conditions = get_filter_query_conditions(self.search_fields, query)

        # TODO add filter by user when will be perfect note model
        query_set = self.model.objects.filter(
            # and_(self.model.user == self.request.user, (
            filter_conditions
            # )
        )
        return query_set
