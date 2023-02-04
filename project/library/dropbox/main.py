import os
from pathlib import Path
import logging

import dropbox
from dropbox.exceptions import ApiError

dbx = dropbox.Dropbox(os.environ.get("DROPBOX_TOKEN"))


def upload_file_to_dropbox(file: Path, upload_file_path: str) -> str:
    """
    Uploads given givel to dropbox cloud
    :param file: file path which must be uploaded
    :param upload_file_path: path where file will be stored
    :return: unique identifier for the file.
    """
    with open(file, "rb") as f:
        try:
            response = dbx.files_upload(f.read, upload_file_path, )
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().reason.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
    return response.id
