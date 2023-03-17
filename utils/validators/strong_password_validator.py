import re


def password_validator(password: str) -> bool:
    # Must be between 6 and 20 characters long.
    regex = r"^.{6,20}$"
    if not re.match(regex, password):
        return False

    return True
