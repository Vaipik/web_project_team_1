from django.conf import settings
from dotenv import dotenv_values

env = dotenv_values(settings.BASE_DIR.parent / ".env")

dropbox_env = {
    k: env[k] for k in env if k.startswith("DROPBOX")
}
dropbox_env["DROPBOX_ROOT_PATH"] = "/tests"
