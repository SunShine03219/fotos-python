import pytest

from tests.conftest import drop_database
from tests.schemas_tests.users_tests_schemas import (
    ADMIN_LOGIN,
    DEFAULT_ADMIN,
    DEFAULT_USER,
    UPDATE_USER,
    USER_LOGIN,
)


@pytest.mark.integration
@pytest.mark.low
@pytest.mark.asyncio
@drop_database
async def test_create_valid_user(client_with_db):
    token = await client_with_db.post("/login/", json=DEFAULT_ADMIN)
    header = {"Authorization": f"Bearer {token.json()['access_token']}"}

    response = await client_with_db.post(
        "/users/", json=DEFAULT_USER, headers=header
    )

    assert response.status_code == 201
    assert response.json()["name"] == DEFAULT_USER["name"]
    assert response.json()["email"] == DEFAULT_USER["email"]


@pytest.mark.integration
@pytest.mark.high
@pytest.mark.asyncio
@drop_database
async def test_create_invalid_user(client_with_db):
    token = await client_with_db.post("/login/", json=DEFAULT_ADMIN)
    header = {"Authorization": f"Bearer {token.json()['access_token']}"}

    response_ok = await client_with_db.post(
        "/users/", json=DEFAULT_USER, headers=header
    )
    response_fail = await client_with_db.post(
        "/users/", json=DEFAULT_USER, headers=header
    )

    assert response_ok.status_code == 201
    assert response_fail.status_code == 400


@pytest.mark.integration
@pytest.mark.high
@pytest.mark.asyncio
@drop_database
async def test_update_valid_user_id(client_with_db):
    token = await client_with_db.post("/login/", json=DEFAULT_ADMIN)
    header = {"Authorization": f"Bearer {token.json()['access_token']}"}
    await client_with_db.post("/users/", json=DEFAULT_USER, headers=header)

    response_by_admin = await client_with_db.patch(
        "/users/2", json=UPDATE_USER, headers=header
    )

    token = await client_with_db.post("/login/", json=DEFAULT_USER)
    header = {"Authorization": f"Bearer {token.json()['access_token']}"}
    response_by_default = await client_with_db.patch(
        "/users/2", json=UPDATE_USER, headers=header
    )

    assert response_by_admin.status_code == 204
    assert response_by_default.status_code == 204


@pytest.mark.integration
@pytest.mark.high
@pytest.mark.asyncio
@drop_database
async def test_update_valid_user_admin_id(client_with_db):
    token_admin = await client_with_db.post("/login/", json=DEFAULT_ADMIN)
    header_admin = {
        "Authorization": f"Bearer {token_admin.json()['access_token']}"
    }
    await client_with_db.post(
        "/users/", json=DEFAULT_USER, headers=header_admin
    )

    response_by_admin = await client_with_db.patch(
        "/users/1", json=UPDATE_USER, headers=header_admin
    )

    token_default = await client_with_db.post("/login/", json=DEFAULT_USER)
    header_default = {
        "Authorization": f"Bearer {token_default.json()['access_token']}"
    }
    response_by_default = await client_with_db.patch(
        "/users/1", json=UPDATE_USER, headers=header_default
    )

    assert response_by_admin.status_code == 204
    assert response_by_default.status_code == 401


@pytest.mark.integration
@pytest.mark.high
@pytest.mark.asyncio
@drop_database
async def test_update_invalid_user_id(client_with_db):
    token_admin = await client_with_db.post("/login/", json=DEFAULT_ADMIN)
    header_admin = {
        "Authorization": f"Bearer {token_admin.json()['access_token']}"
    }
    await client_with_db.post(
        "/users/", json=DEFAULT_USER, headers=header_admin
    )

    token = await client_with_db.post("/login/", json=USER_LOGIN)
    header = {"Authorization": f"Bearer {token.json()['access_token']}"}
    response_fail = await client_with_db.patch(
        "/users/100", json=UPDATE_USER, headers=header
    )

    assert response_fail.status_code == 404


@pytest.mark.integration
@pytest.mark.high
@pytest.mark.asyncio
@drop_database
async def test_get_one_valid_user(client_with_db):
    token_admin = await client_with_db.post("/login/", json=DEFAULT_ADMIN)
    header_admin = {
        "Authorization": f"Bearer {token_admin.json()['access_token']}"
    }
    await client_with_db.post(
        "/users/", json=DEFAULT_USER, headers=header_admin
    )
    response = await client_with_db.get("/users/2")

    assert response.status_code == 200
    assert response.json()["name"] == DEFAULT_USER["name"]
    assert response.json()["email"] == DEFAULT_USER["email"]


@pytest.mark.integration
@pytest.mark.high
@pytest.mark.asyncio
async def test_get_one_invalid_user(client_with_db):
    response_fail = await client_with_db.get("/users/100")

    assert response_fail.status_code == 404


@pytest.mark.integration
@pytest.mark.high
@pytest.mark.asyncio
@drop_database
async def test_get_valid_users_list(client_with_db):
    token = await client_with_db.post("/login/", json=ADMIN_LOGIN)
    header = {"Authorization": f"Bearer {token.json()['access_token']}"}

    response = await client_with_db.get("/users/", headers=header)

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.integration
@pytest.mark.high
@pytest.mark.asyncio
@drop_database
async def test_delete_valid_user_by_id(client_with_db):
    token = await client_with_db.post("/login/", json=ADMIN_LOGIN)
    header = {"Authorization": f"Bearer {token.json()['access_token']}"}
    response = await client_with_db.delete("/users/1", headers=header)

    assert response.status_code == 204


@pytest.mark.integration
@pytest.mark.high
@pytest.mark.asyncio
@drop_database
async def test_delete_invalid_user_by_id(client_with_db):
    token = await client_with_db.post("/login/", json=ADMIN_LOGIN)
    header = {"Authorization": f"Bearer {token.json()['access_token']}"}
    response_fail = await client_with_db.delete("/users/100", headers=header)

    assert response_fail.status_code == 404


@pytest.mark.integration
@pytest.mark.high
@pytest.mark.asyncio
@drop_database
async def test_delete_with_invalid_token_user(client_with_db):
    token = await client_with_db.post("/login/", json=ADMIN_LOGIN)
    header = {"Authorization": f"Bearer {token.json()['access_token']}test"}
    response_fail = await client_with_db.delete("/users/1", headers=header)

    assert response_fail.status_code == 401


@pytest.mark.integration
@pytest.mark.high
@pytest.mark.asyncio
@drop_database
async def test_get_me_user(client_with_db):
    token = await client_with_db.post("/login/", json=ADMIN_LOGIN)
    header = {"Authorization": f"Bearer {token.json()['access_token']}"}
    response = await client_with_db.get("/users/me", headers=header)

    assert response.status_code == 200
