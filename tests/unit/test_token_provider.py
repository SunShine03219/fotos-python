import pytest

from utils.exceptions.exception import UnauthorizedLogin
from utils.providers.token_provider import jwt_encoder, verify_jwt_token


@pytest.mark.unit
@pytest.mark.high
def test_verify_valid_token():
    data = {"sub": "user@example.com", "name": "John Doe"}
    token = jwt_encoder(data)
    payload = verify_jwt_token(token)
    assert payload["sub"] == data["sub"]


@pytest.mark.unit
@pytest.mark.high
def test_verify_invalid_token():
    token = "invalid-token"
    with pytest.raises(UnauthorizedLogin):
        verify_jwt_token(token)
