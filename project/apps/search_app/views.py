from operator import and_

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.db.models import Q, QuerySet
from django.shortcuts import redirect
from django.views.generic import ListView

from .utils import get_filter_query_conditions, SearchAppMixin
from utils.pagination import PaginationMixin
from ..contacts.models import Contact
from ..file_storage.models import File
from ..notes.models import Note


class SearchContactView(LoginRequiredMixin, PaginationMixin, SearchAppMixin, ListView):
    """
    "model" - model class name for search
    "search_fields" - model fields for search. It should be CharField type or ArrayField type of CharField type
    "fields" - model fields for show in template.
    "auth_required" - if model stores personal users data,
        True - require authentication, if True there must be declare model field name related to User
        False - not require authentication
    "user_model_name" - model field name related to User
    "url_name" - url name for url tag that link to item page by uuid
    "uuid" - model field name with unique item id
    """
    model = Contact
    search_fields = ["name",
                     "address",
                     "emails__email_addr",
                     "phones__phone_number",
                     ]
    fields = ["name",
              "address",
              "emails__email_addr",
              "phones__phone_number",
              ]
    auth_required = True
    user_model_name = "owner"
    url_name = "contacts:update_contact"
    uuid = "id"


class SearchFileView(LoginRequiredMixin, PaginationMixin, SearchAppMixin, ListView):
    model = File
    search_fields = ["description",
                     ]
    fields = ["description",
              "uploaded_at",
              "category",
              ]
    auth_required = True
    user_model_name = "owner"
    url_name = "file_storage:show_file"
    uuid = "uuid"


class SearchNoteView(LoginRequiredMixin, PaginationMixin, SearchAppMixin, ListView):
    model = Note
    search_fields = ["name",
                     "description",
                     "tags__name",
                     ]
    fields = ["name",
              "description",
              "tags__name",
              "created_at"
              ]
    auth_required = True
    user_model_name = "user"
    url_name = "notes:detail"
    uuid = "uuid"


class SearchUniView(LoginRequiredMixin, PaginationMixin, ListView):
    paginate_by = 3
    extra_context = {"title": "Search for all categories"}
    template_name = "search_app/search_results.html"

    query_name = "query"
    models = [
        {
            "model": SearchContactView.model,
            "search_fields": SearchContactView.search_fields,
            "fields": SearchContactView.fields,
            "auth_required": SearchContactView.auth_required,
            "user_model_name": SearchContactView.user_model_name,
            "url_name": SearchContactView.url_name,
            "uuid": SearchContactView.uuid
        },
        {
            "model": SearchFileView.model,
            "search_fields": SearchFileView.search_fields,
            "fields": SearchFileView.fields,
            "auth_required": SearchFileView.auth_required,
            "user_model_name": SearchFileView.user_model_name,
            "url_name": SearchFileView.url_name,
            "uuid": SearchFileView.uuid
        },
        {
            "model": SearchNoteView.model,
            "search_fields": SearchNoteView.search_fields,
            "fields": SearchNoteView.fields,
            "auth_required": SearchNoteView.auth_required,
            "user_model_name": SearchNoteView.user_model_name,
            "url_name": SearchNoteView.url_name,
            "uuid": SearchNoteView.uuid
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
                query_set = model_class.objects.filter(
                    Q(**{model['user_model_name']: self.request.user})
                    & filter_conditions).distinct()
            else:
                query_set = model_class.objects.filter(filter_conditions).distinct()

            object_list.append((model_class.__name__,
                                model["fields"],
                                model['url_name'],
                                model['uuid'],
                                query_set,
                                ))

        return object_list


