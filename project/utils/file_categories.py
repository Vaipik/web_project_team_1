from enum import Enum
from pathlib import Path

from django.utils import timezone


class Categories(Enum):
    """Allowed file categories and their extensions"""
    IMAGES = ("jpeg", "png", "jpg", "svg")
    VIDEOS = ("mp4", "mov", "mkv")
    DOCUMENTS = ("doc", "docx", "txt", "pdf", "xlsx", "pptx")
    AUDIO = ("mp3", "ogg", "wav", "amr")
    ARCHIVES = ("zip", "gz", "tar")


def _get_folder_name(instance, filename) -> str:
    """
    Creating folder with name according to category with year, month, day additions
    :param instance: instance of django model with FileField
    :param filename:
    :return: str for FileFields upload_to
    """
    extension = Path(filename).suffix[1:]

    for category in Categories:
        if extension in category.value:
            folder_type = category.name
            break

    new_filename = f"{instance.uuid}.{extension}"  # UUID.EXT
    # Will be converted in models.FileField
    date_path = instance.uploaded_at.date() if hasattr(instance, "uploaded_at") else timezone.now().date()
    path = f"{folder_type}/{date_path}/{new_filename}"  # MEDIA/created_date/UUID.EXT
    return path

