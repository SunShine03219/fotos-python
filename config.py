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
    TYPE = getenv("TYPE")
    PROJECT_ID = getenv("PROJECT_ID")
    PRIVATE_KEY_ID = getenv("PRIVATE_KEY_ID")
    PRIVATE_KEY = getenv("PRIVATE_KEY")
    CLIENT_EMAIL = getenv("CLIENT_EMAIL")
    CLIENT_ID = getenv("CLIENT_ID")
    AUTH_URI = getenv("AUTH_URI")
    TOKEN_URI = getenv("TOKEN_URI")
    AUTH_PROVIDER_x509_CERT_URL = getenv("AUTH_PROVIDER_x509_CERT_URL")
    CLIENT_x509_CERT_URL = getenv("CLIENT_x509_CERT_URL")
