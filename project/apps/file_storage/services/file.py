from uuid import UUID

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models import QuerySet
from django.core.files import File as CoreFile

from ..models import File
from ..tasks import upload_file_task

User = settings.AUTH_USER_MODEL


def upload_file(**kwargs) -> None:
    """
    Creating category if it does not exist and uploads a file
    :param kwargs: kwargs received from file upload form
    :return: None
    """
    file = kwargs["file"]  # 100% will be in kwargs, because kwargs is valid data from upload form

    # category = get_file_category(filename.name)   # original code
    # File.objects.create(**kwargs, category=category)     # original code

    storage = FileSystemStorage()

    storage.save(file.name, CoreFile(file))

    path = storage.path(file.name)

    upload_file_task.delay(path,
                           file.name,
                           kwargs['description'],
                           kwargs['owner'].pk)


def get_user_files(owner: User) -> QuerySet[File]:
    files = File.objects.select_related("category").filter(owner=owner)
    return files


def get_file(file_uuid: UUID) -> File:
    file = File.objects.get(uuid=file_uuid)
    return file


def get_user_category_files(user: User, category_url: str) -> QuerySet[File]:
    files = File.objects.select_related("category"). \
        filter(category__slug=category_url, owner=user)
    return files



