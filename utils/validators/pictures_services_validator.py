import re


def file_or_folder_validator(path: str = "") -> bool:
    if re.match(r"^(.*\/)?([^\/]*\..+)?$|^.*\/$", path):
        if path.endswith("/"):
            return True
        else:
            return False
    return True
