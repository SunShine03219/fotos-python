from os import getenv

from dotenv import load_dotenv


class SingletonMeta(type):
    """
    Singleton class for instantiate only one time the configs.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


def _verify_credentials(credentials: dict):
    return True if "" in credentials.values() else False


class Config(metaclass=SingletonMeta):
    """
    Loading .env file and other configs to be able to get it in all project.
    """

    load_dotenv()
    production_mode = getenv("PRODUCTION_MODE", default=True)
    SECRET_KEY = getenv("SECRET_KEY", default="secret")
    DATABASE_URL = getenv("DATABASE_URL")
    DATABASE_TEST_URL = getenv("DATABASE_TEST_URL")

    # Google Cloud Service Account Access Credentials
    CREDENTIALS: dict = {
        "type": getenv("TYPE", default=""),
        "project_id": getenv("PROJECT_ID", default=""),
        "private_key_id": getenv("PRIVATE_KEY_ID", default=""),
        "private_key": getenv("PRIVATE_KEY", default=""),
        "client_email": getenv("CLIENT_EMAIL", default=""),
        "client_id": getenv("CLIENT_ID", default=""),
        "auth_uri": getenv("AUTH_URI", default=""),
        "token_uri": getenv("TOKEN_URI", default=""),
        "auth_provider_x509_cert_url": getenv(
            "AUTH_PROVIDER_x509_CERT_URL", default=""
        ),
        "client_x509_cert_url": getenv("CLIENT_x509_CERT_URL", default=""),
    }

    IS_EMPTY = _verify_credentials(CREDENTIALS)

    BUCKET_NAME = getenv("BUCKET_NAME")
