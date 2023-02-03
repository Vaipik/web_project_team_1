from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^files/", include("apps.file_storage.urls", namespace="file_storage")),
    re_path(r"^auth/", include("apps.user_auth.urls", namespace="user_auth")),
    re_path(r"^contacts/", include('apps.contacts.urls', namespace="contacts")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
