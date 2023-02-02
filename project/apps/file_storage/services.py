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
