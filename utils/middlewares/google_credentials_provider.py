from config import Config
from google.cloud import storage


def get_cloud_storage_client():
    if Config.IS_EMPTY:
        return None

    client = storage.Client.from_service_account_info(info=Config.CREDENTIALS)

    return client
