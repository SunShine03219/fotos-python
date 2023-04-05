import mimetypes
import os
import shutil
import tempfile
from typing import List
from urllib.parse import quote

from config import Config
from fastapi import Response, UploadFile
from fastapi.responses import FileResponse
from google.cloud.exceptions import GoogleCloudError

from utils.exceptions.exception import (
    FileDownloadError,
    FileUploadError,
    InvalidCredentials,
    InvalidPathOrFile,
)
from utils.middlewares.files_service import create_tree, get_new_name
from utils.middlewares.google_credentials_provider import (
    get_cloud_storage_client,
)

client = get_cloud_storage_client()


class Pictures:
    @staticmethod
    async def get_files_path(file_path: str = ""):
        if client:
            bucket = client.get_bucket(Config.BUCKET_NAME)
            blob = bucket.blob(blob_name=file_path)
            if file_path:
                prefix = (
                    blob.name if blob.name.endswith("/") else f"{blob.name}/"
                )
            else:
                prefix = ""
            blobs = bucket.list_blobs(prefix=prefix)
            file_list = [
                b
                for b in blobs
                if b.name != prefix
            ]
            if not file_list:
                raise InvalidPathOrFile(f"Invalid path: '{file_path}'")
            tree = create_tree(file_list, file_path, prefix)
            return tree
        else:
            raise InvalidCredentials("Is there any empty credential")

    @staticmethod
    async def get_file_source(file_path: str):
        if client:
            bucket = client.get_bucket(Config.BUCKET_NAME)
            blob = bucket.blob(blob_name=file_path)

            if not blob.exists():
                raise InvalidPathOrFile(f"Invalid file: '{file_path}'")

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
        bucket = client.get_bucket(Config.BUCKET_NAME)
        update_path = {}
        count = 1

        for file in files:
            path, item = os.path.split(file.filename)
            if path in update_path:
                file.filename = file.filename.replace(path, update_path[path])
            blob_name = (
                f"{file_path}/{file.filename}" if file_path else file.filename
            )
            blob = bucket.blob(blob_name)
            while blob.exists():
                if path:
                    update_path[path] = get_new_name(path, count)
                    count += 1
                else:
                    file.filename = get_new_name(file.filename, count)
                    count += 1
                blob_name = (
                    f"{file_path}/{file.filename}"
                    if file_path
                    else file.filename
                )
                blob = bucket.blob(blob_name)
            count = 1
            try:
                blob.upload_from_string(
                    await file.read(), content_type=file.content_type
                )
            except GoogleCloudError as e:
                raise FileUploadError(
                    f"Error sending file {file.filename}: {e}"
                )
        return {"SUCCESS_UPLOAD": "End of upload service"}

    @staticmethod
    async def create_folder(folder_path: str = ""):
        bucket = client.get_bucket(Config.BUCKET_NAME)
        blob = bucket.blob(folder_path)
        try:
            blob.upload_from_string('', content_type='application/x-www-form-urlencoded;charset=UTF-8')
        except GoogleCloudError as e:
            raise FileUploadError(
                f"Error creating folder {folder_path}: {e}"
            )
        return {"SUCCESS_UPLOAD": "End of upload service"}

    @staticmethod
    async def delete_file(file_path: str):
        if client:
            bucket = client.get_bucket(Config.BUCKET_NAME)
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
            bucket = client.get_bucket(Config.BUCKET_NAME)
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

    @staticmethod
    async def download_file(file_path: str):
        if client:
            bucket = client.get_bucket(Config.BUCKET_NAME)
            blob = bucket.blob(blob_name=file_path)
            if blob.exists():
                try:
                    media_type, encoding = mimetypes.guess_type(blob.name)
                    return Response(
                        content=blob.download_as_bytes(),
                        media_type="application/octet-stream",
                        headers={
                            "Content-Disposition": f"attachment;"
                            f' filename="{os.path.basename(blob.name)}"',
                            "Content-Type": f"{media_type}",
                        },
                    )
                except GoogleCloudError as e:
                    raise FileDownloadError(
                        f"Error downloading file "
                        f"{os.path.basename(blob.name)}: {e}"
                    )
            else:
                raise InvalidPathOrFile(
                    f"File {os.path.basename(blob.name)} does not exist"
                )
        else:
            raise InvalidCredentials("Is there any empty credential")

    @staticmethod
    async def download_folder(file_path: str):
        if client:
            bucket = client.get_bucket(Config.BUCKET_NAME)
            blobs = list(bucket.list_blobs(prefix=file_path))
            if blobs:
                with tempfile.TemporaryDirectory() as temp_dir:
                    for blob in blobs:
                        file_name = os.path.join(temp_dir, blob.name)
                        os.makedirs(os.path.dirname(file_name), exist_ok=True)
                        blob.download_to_filename(file_name)
                    shutil.make_archive(temp_dir, "zip", temp_dir)
                    return FileResponse(
                        f"{temp_dir}.zip",
                        media_type="application/zip",
                        filename=f"{os.path.basename(file_path)}.zip",
                    )
            else:
                raise InvalidPathOrFile(
                    f"Folder {os.path.basename(file_path)} does not exist"
                )
        else:
            raise InvalidCredentials("Is there any empty credential")
