from operator import and_

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.shortcuts import redirect
from django.views.generic import ListView

from .models import TempNote, TempContact
from ..contacts.models import Contact
from .utils import get_filter_query_conditions, SearchAppMixin
from utils.pagination import PaginationMixin


class SearchUniView(LoginRequiredMixin, PaginationMixin, ListView):
    template_name = "search_app/search_results.html"
    """
    "model" - model class name for search
    "search_fields" - model fields for search. It should be CharField type or ArrayField type of CharField type
    "auth_required" - if model stores personal users data, 
        True - require authentication, 
        False - not require authentication 
    """
    models = [
        {
            "model": "TempNote",
            "search_fields": ["description",
                              "text",
                              "tags"],
            "auth_required": False
        },
        {
            "model": "TempContact",
            "search_fields": ["description",
                              "text",
                              "tags"],
            "auth_required": False
        },
        {
            "model": "Contact",
            "search_fields": ["name",
                              "address",
                              "phones"],
            "auth_required": False
        },
    ]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        query_string = self.request.GET.get("search", None)
        if query_string:
            query_list = query_string.split()
            context.update({"query": query_list})

        context.update(
            **self.get_pages(page_obj=context["page_obj"]),
        )
        return context

    def get_queryset(self):
        query = self.request.GET.get("search", None)
        if query is None:
            messages.error(self.request, "Please enter some keyword to search")
            redirect(self.request.META.get("HTTP_REFERER"))

        object_list = []
        for model in self.models:

            filter_conditions = get_filter_query_conditions(model["search_fields"], query)

            model_class = globals()[model["model"]] if isinstance(model["model"], str) else model["model"]

            if model["auth_required"]:
                query_set = model_class.objects.filter(and_(model_class.user == self.request.user, filter_conditions))
            else:
                query_set = model_class.objects.filter(filter_conditions)

            object_list.append((model_class.__name__, model["search_fields"], query_set))

        return object_list


class SearchContactView(LoginRequiredMixin, PaginationMixin, SearchAppMixin,  ListView):
    template_name = "search_app/search_contacts.html"
    """
    "model" - model class name for search
    "search_fields" - model fields for search. It should be CharField type or ArrayField type of CharField type
    "auth_required" - if model stores personal users data, 
        True - require authentication, 
        False - not require authentication 
    """
    model = {
            "model": "Contact",
            "search_fields": ["name",
                              "address",
                              "phones"],
            "auth_required": False
        }
