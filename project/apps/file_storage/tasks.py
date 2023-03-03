from pathlib import Path

from celery import shared_task
from django.core.files.storage import FileSystemStorage
from django.core.files import File as CoreFile

from .models import File
from .services.file_categories import get_file_category, get_owner


@shared_task(bind=True, name='upload_file_task')
def upload_file_task(bind, path, filename, description, owner_id):
    print('Uploading file...')

    storage = FileSystemStorage()

    path_object = Path(path)

    category = get_file_category(filename)

    owner = get_owner(owner_id)

    with open(path_object, mode='rb') as file:
        file_instance = CoreFile(file, name=path_object.name)
        File.objects.create(description=description,
                            file=file_instance,
                            category=category,
                            owner=owner)

    storage.delete(filename)

    print('File upload')
