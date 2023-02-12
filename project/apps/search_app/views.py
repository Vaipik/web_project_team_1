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


class SearchUniView(LoginRequiredMixin, PaginationMixin, ListView):
    paginate_by = 1
    extra_context = {"title": "Search for all categories"}
    template_name = "search_app/search_results.html"

    """
    "model" - model class name for search
    "search_fields" - model fields for search. It should be CharField type or ArrayField type of CharField type
    "fields" - model fields for show in template.
    "auth_required" - if model stores personal users data, 
        True - require authentication, if True there must be declare model field name related to User
        False - not require authentication 
    "user_model_name" - model field name related to User
    """
    query_name = "query"
    models = [
        {
            "model": Contact,
            "search_fields": ["name",
                              "address",
                              ],
            "fields": ["name",
                       "address",
                       "birthday",
                       "sex",
                       ],
            "auth_required": False,
            "user_model_name": "owner",
        },
        {
            "model": File,
            "search_fields": ["description",
                              ],
            "fields": ["description",
                       "uploaded_at",
                       "category",
                       ],
            "auth_required": True,
            "user_model_name": "owner",
        },
        {
            "model": Note,
            "search_fields": ["name",
                              "description",
                              ],
            "fields": ["name",
                       "description",
                       "created_at",
                       "edited_at",
                       ],
            "auth_required": True,
            "user_model_name": "user",
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
                    & filter_conditions)
            else:
                query_set = model_class.objects.filter(filter_conditions)

            object_list.append((model_class.__name__, model["fields"], query_set))

        return object_list


class SearchContactView(LoginRequiredMixin, PaginationMixin, SearchAppMixin, ListView):
    """
    "model" - model class name for search
    "search_fields" - model fields for search. It should be CharField type or ArrayField type of CharField type
    "fields" - model fields for show in template.
    "auth_required" - if model stores personal users data, 
        True - require authentication, if True there must be declare model field name related to User
        False - not require authentication
    "user_model_name" - model field name related to User
    """
    model = Contact
    search_fields = ["name",
                     "address",
                     ]
    fields = ["name",
              "address",
              ]
    auth_required = False
    user_model_name = "owner"


class SearchFileView(LoginRequiredMixin, PaginationMixin, SearchAppMixin, ListView):
    """
    "model" - model class name for search
    "search_fields" - model fields for search. It should be CharField type or ArrayField type of CharField type
    "fields" - model fields for show in template.
    "auth_required" - if model stores personal users data,
        True - require authentication, if True there must be declare model field name related to User
        False - not require authentication
    "user_model_name" - model field name related to User
    """
    model = File
    search_fields = ["description",
                     ]
    fields = ["description",
              ]
    auth_required = True
    user_model_name = "owner"


class SearchNoteView(LoginRequiredMixin, PaginationMixin, SearchAppMixin, ListView):
    """
    "model" - model class name for search
    "search_fields" - model fields for search. It should be CharField type or ArrayField type of CharField type
    "fields" - model fields for show in template.
    "auth_required" - if model stores personal users data,
        True - require authentication, if True there must be declare model field name related to User
        False - not require authentication
    "user_model_name" - model field name related to User
    """
    model = Note
    search_fields = ["name",
                     "description",
                     ]
    fields = ["name",
              "description",
              ]
    auth_required = True
    user_model_name = "user"
