from django.db.models import Q


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
    paginate_by = 3
    template_name = "search_app/search_model_result.html"
    extra_context = {"title": "Search"}

    query_name = "query"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        query_string = self.request.GET.get(self.query_name, None)
        if query_string:
            context.update({"query": query_string})

        context.update({"model_name": self.model.__name__,
                        "fields": self.fields,
                        "url_name": self.url_name,
                        "uuid": self.uuid})

        context.update(
            **self.get_pages(page_obj=context["page_obj"]),
        )

        return context

    def get_queryset(self):
        query = self.request.GET.get(self.query_name, None)

        filter_conditions = get_filter_query_conditions(self.search_fields, query)

        if self.auth_required:
            query_set = self.model.objects.filter(
                Q(**{self.user_model_name: self.request.user})
                & filter_conditions).distinct()
        else:
            query_set = self.model.objects.filter(filter_conditions).distinct()

        return query_set
