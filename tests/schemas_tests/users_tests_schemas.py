from persistency.schemas.user_schemas import RoleOptions

DEFAULT_USER = {
    "name": "Default User",
    "email": "default_user@test.com",
    "password": "SenhaDefault",
    "role": RoleOptions.Default,
}

DEFAULT_ADMIN = {
    "name": "Default Admin",
    "email": "admin_user@test.com",
    "password": "SenhaAdmin",
    "role": RoleOptions.Admin,
}

UPDATE_USER = {"name": "Update User"}

USER_LOGIN = {
    "email": DEFAULT_USER["email"],
    "password": DEFAULT_USER["password"],
}

ADMIN_LOGIN = {
    "email": DEFAULT_ADMIN["email"],
    "password": DEFAULT_ADMIN["password"],
}
