import mimetypes
from typing import List
from urllib.parse import quote

from fastapi import Response, UploadFile
from google.cloud.exceptions import GoogleCloudError

from utils.exceptions.exception import (
    FileUploadError,
    InvalidCredentials,
    InvalidPathOrFile,
)
from utils.middlewares.files_service import create_tree
from utils.middlewares.google_credentials_provider import (
    get_cloud_storage_client,
)

client = get_cloud_storage_client()


class Pictures:
    @staticmethod
    async def get_files_path(file_path: str = ""):
        if client:
            bucket = client.get_bucket("testes-roque")
            blob = bucket.blob(blob_name=file_path)

            blobs = bucket.list_blobs(prefix=blob.name)
            file_list = [quote(b.name) for b in blobs if b.name != blob.name]
            tree = create_tree(file_list, file_path)
            return tree
        else:
            raise InvalidCredentials("Is there any empty credential")

    @staticmethod
    async def get_file_source(file_path: str):
        if client:
            bucket = client.get_bucket("testes-roque")
            blob = bucket.blob(blob_name=file_path)

            try:
                media_type, encoding = mimetypes.guess_type(blob.name)
                return Response(
                    content=blob.download_as_bytes(),
                    media_type="application/octet-stream",
                    headers={
                        "Content-Disposition": f"inline;"
                        f' filename="{blob.name}"',
                        "Content-Type": f"{media_type}",
                    },
                )
            except Exception as e:
                return {"Error": e}
        else:
            raise InvalidCredentials("Is there any empty credential")

    @staticmethod
    async def upload_files(files: List[UploadFile], file_path: str = ""):
        bucket = client.get_bucket("testes-roque")
        for file in files:
            try:
                blob_name = (
                    f"{file_path}/{file.filename}"
                    if file_path
                    else file.filename
                )
                blob = bucket.blob(blob_name)
                blob.upload_from_string(
                    await file.read(), content_type=file.content_type
                )
            except GoogleCloudError as e:
                raise FileUploadError(
                    f"Error sending file {file.filename}: {e}"
                )
        return {"SUCCESS_UPLOAD": "End of upload service"}

    @staticmethod
    async def delete_file(file_path: str):
        if client:
            bucket = client.get_bucket("testes-roque")
            blob = bucket.blob(blob_name=file_path)
            if not blob.exists():
                raise InvalidPathOrFile(f"File '{file_path}' not found.")
            blob.delete()
            return {
                "SUCCESS_DELETE": f"File '{file_path}' deleted successfully."
            }
        else:
            raise InvalidCredentials("Is there any empty credential")

    @staticmethod
    async def delete_folder(folder_path: str):
        if client:
            bucket = client.get_bucket("testes-roque")
            blobs = list(bucket.list_blobs(prefix=folder_path))
            if not blobs:
                raise InvalidPathOrFile(f"Folder '{folder_path}' not found.")
            for blob in blobs:
                blob.delete()
            return {
                "SUCCESS_DELETE": f"Folder '{folder_path}'"
                f" deleted successfully."
            }
        else:
            raise InvalidCredentials("Is there any empty credential")
