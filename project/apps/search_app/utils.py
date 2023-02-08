from operator import and_

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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        query_string = self.request.GET.get("search", None)
        if query_string:
            query_list = query_string.split()
            context.update({"query": query_list})

        context.update(
            **self.get_pages(page_obj=context["page_obj"]),
        )

        model_class = globals()[self.model["model"]] if isinstance(self.model["model"], str) else self.model["model"]
        context.update({"model_name": model_class.__name__, "fields": self.model["search_fields"]})

        return context

    def get_queryset(self):
        query = self.request.GET.get("search", None)
        if query is None:
            messages.error(self.request, "Please enter some keyword to search")
            redirect(self.request.META.get("HTTP_REFERER"))

        filter_conditions = get_filter_query_conditions(self.model["search_fields"], query)

        model_class = globals()[self.model["model"]] if isinstance(self.model["model"], str) else self.model["model"]

        if self.model["auth_required"]:
            query_set = model_class.objects.filter(and_(model_class.user == self.request.user, filter_conditions))
        else:
            query_set = model_class.objects.filter(filter_conditions)

        return query_set
