from operator import and_

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.db.models import Q, QuerySet
from django.shortcuts import redirect
from django.views.generic import ListView

from .models import TempNote, TempContact
from ..contacts.models import Contact
from .utils import get_filter_query_conditions, SearchAppMixin
from utils.pagination import PaginationMixin

from ..file_storage.models import File


class SearchUniView(LoginRequiredMixin, PaginationMixin, ListView):
    paginate_by = 1
    extra_context = {"title": "Search for all categories"}
    template_name = "search_app/search_results.html"

    """
    "model" - model class name for search
    "search_fields" - model fields for search. It should be CharField type or ArrayField type of CharField type
    "auth_required" - if model stores personal users data, 
        True - require authentication, 
        False - not require authentication 
    """
    query_name = "query"
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
        {
            "model": File,
            "search_fields": ["description",
                              ],
            "auth_required": False
        },
    ]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        query_string = self.request.GET.get(self.query_name, None)
        if query_string:
            context.update({"query": query_string})

        context.update(
            **self.get_pages(page_obj=context["page_obj"]),
        )

        return context

    def get_queryset(self):
        query = self.request.GET.get(self.query_name, None)
        if query is None:
            messages.error(self.request, "Please enter some keyword to search")
            redirect(self.request.META.get("HTTP_REFERER"))

        object_list = []
        for model in self.models:

            filter_conditions = get_filter_query_conditions(model["search_fields"], query)

            model_class = globals()[model["model"]] if isinstance(model["model"], str) else model["model"]

            if model["auth_required"]:
                query_set = model_class.objects.filter(Q(owner=self.request.user) & filter_conditions)
            else:
                query_set = model_class.objects.filter(filter_conditions)

            object_list.append((model_class.__name__, model["search_fields"], query_set))

        return object_list


class SearchContactView(LoginRequiredMixin, PaginationMixin, SearchAppMixin, ListView):
    """
    "model" - model class name for search
    "search_fields" - model fields for search. It should be CharField type or ArrayField type of CharField type
    "auth_required" - if model stores personal users data, 
        True - require authentication, 
        False - not require authentication 
    """
    model = Contact
    search_fields = ["name",
                     "address",
                     "phones"],
    auth_required = False


class SearchFileView(LoginRequiredMixin, PaginationMixin, SearchAppMixin, ListView):
    """
    "model" - model class name for search
    "search_fields" - model fields for search. It should be CharField type or ArrayField type of CharField type
    "auth_required" - if model stores personal users data,
        True - require authentication,
        False - not require authentication
    """
    model = File
    search_fields = ["description",
                     ]
    auth_required = True
