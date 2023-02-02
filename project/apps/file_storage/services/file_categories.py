from pathlib import Path

from ..models import Categories, FileCategory


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


def get_file_category(file: str) -> FileCategory:
    """

    :param file:
    :return:
    """
    category_name = determine_file_category(file)
    category, created = FileCategory.objects.get_or_create(name=category_name)
    return category

