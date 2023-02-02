from pathlib import Path

from .models import File, FileCategory, Categories


def determine_file_category(file: str) -> str | None:
    """
    Is used to get file extension and determine folder name
    :param file: file which extension must be checked
    :return: folder name if extension in approved folders or None
    """
    extension = Path(file).suffix[1:]
    for category in Categories:
        if extension in category.value:
            return category.name.lower()


def upload_file(**kwargs) -> None:
    """
    Creating category if it does not exist and uploads a file
    :param kwargs: kwargs received from file upload form
    :return: None
    """
    filename = kwargs["file"]  # 100% will be in kwargs, because kwargs is valid data from upload form
    file_category = determine_file_category(filename.name)

    category, created = FileCategory.objects.get_or_create(name=file_category)
    File.objects.create(**kwargs, category=category)
