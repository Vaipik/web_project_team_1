from uuid import UUID

from django.conf import settings
from django.db.models import QuerySet

from ..models import File, FileCategory
from ..libs.queries import query_debugger
from .file_categories import get_file_category

User = settings.AUTH_USER_MODEL


def upload_file(**kwargs) -> None:
    """
    Creating category if it does not exist and uploads a file
    :param kwargs: kwargs received from file upload form
    :return: None
    """
    filename = kwargs["file"]  # 100% will be in kwargs, because kwargs is valid data from upload form
    category = get_file_category(filename.name)
    File.objects.create(**kwargs, category=category)


@query_debugger
def get_user_files(owner: User) -> QuerySet[File]:
    files = File.objects.select_related("category").filter(owner=owner)
    return files


def get_file(file_uuid: UUID) -> File:
    file = File.objects.get(uuid=file_uuid)
    return file


def get_user_category_files(user: User, category_url: str) -> QuerySet[File]:
    files = FileCategory.objects.prefetch_related("category").\
        get(slug=category_url).category.filter(owner=user)
    return files
