import pytest

from utils.validators.email_address_validator import email_validator
from utils.validators.strong_password_validator import password_validator


@pytest.mark.unit
@pytest.mark.medium
def test_email_address_valid():
    list_email = ["test@test.com", "test2@gmail.com", "test3@simbiose.com"]
    for email in list_email:
        assert email_validator(email)


@pytest.mark.unit
@pytest.mark.medium
def test_email_address_invalid():
    list_email = ["123", "test@123", "test2@gmail.123", "my_email"]
    for email in list_email:
        assert email_validator(email) is False


@pytest.mark.unit
@pytest.mark.medium
def test_password_validator_valid():
    strong_pass = ["12345aD@", "AGtEssA@!123", "asd@ERF123", "123456"]

    for password in strong_pass:
        assert password_validator(password)


@pytest.mark.unit
@pytest.mark.medium
def test_password_validator_invalid():
    weak_pass = ["12345", "abc", "1", "", "123"]

    for password in weak_pass:
        assert password_validator(password) is False
