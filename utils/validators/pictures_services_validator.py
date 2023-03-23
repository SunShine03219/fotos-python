import re


def file_or_folder_validator(path: str = "") -> bool:
    if re.match(r"^(.*\/)?([^\/]*\..+)?$|^.*\/$", path):
        if path.endswith("/") or not path:
            return True
        else:
            return False
    return True
