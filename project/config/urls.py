from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("apps.search_app.urls", namespace="search_app")),  # it must be first
    re_path(r"^files/", include("apps.file_storage.urls", namespace="file_storage")),
    re_path(r"^auth/", include("apps.user_auth.urls", namespace="user_auth")),
    re_path(r"^notes/", include("apps.notes.urls", namespace="notes")),
    re_path(r'^scrapping/', include('apps.scrapping.urls', namespace='scrapping')),
    re_path(r"^contacts/", include('apps.contacts.urls', namespace="contacts")),
    re_path(r"^about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("", include("apps.user_profile.urls", namespace="user_profile")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
