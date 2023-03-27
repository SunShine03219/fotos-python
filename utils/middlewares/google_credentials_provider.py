from config import Config
from google.cloud import storage
from isort.profiles import google


def get_cloud_storage_client():
    try:
        client = storage.Client.from_service_account_info(
            info=dict(
                type=Config.TYPE,
                project_id=Config.PROJECT_ID,
                private_key_id=Config.PRIVATE_KEY_ID,
                private_key=Config.PRIVATE_KEY,
                client_email=Config.CLIENT_EMAIL,
                client_id=Config.CLIENT_ID,
                auth_uri=Config.AUTH_URI,
                token_uri=Config.TOKEN_URI,
                auth_provider_x509_cert_url=Config.AUTH_PROVIDER_x509_CERT_URL,
                client_x509_cert_url=Config.CLIENT_x509_CERT_URL,
            )
        )
    except google.auth.exceptions.MalformedError:
        client = storage.Client.create_anonymous_client()

    return client
