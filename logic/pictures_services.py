import mimetypes
import os
from typing import List
from urllib.parse import quote

from fastapi import Response, UploadFile
from google.cloud.exceptions import GoogleCloudError

from utils.exceptions.exception import FileUploadError, InvalidCredentials
from utils.middlewares.google_credentials_provider import (
    get_cloud_storage_client,
)

client = get_cloud_storage_client()


class Pictures:
    def _create_tree(file_list: list):
        root = []
        node_dict = {}
        for path in file_list:
            current_node = root
            parts = path.split("/")
            for i, part in enumerate(parts):
                if not part:
                    continue
                if part not in node_dict:
                    node = {
                        "title": part,
                        "content": [] if i != len(parts) - 1 else [],
                    }
                    node_dict[part] = node
                    current_node.append(node)
                current_node = node_dict[part]["content"]
                if isinstance(current_node, dict):
                    break
        if len(file_list) > 0:
            common_prefix = os.path.commonprefix(file_list)
            if common_prefix:
                prefix_parts = common_prefix.split("/")
                for part in prefix_parts[:-1]:
                    if part in node_dict:
                        root = node_dict[part]["content"]
        return root

    async def get_files_path(file_path: str = ""):
        if client:
            bucket = client.get_bucket("testes-roque")
            blob = bucket.blob(blob_name=file_path)

            blobs = bucket.list_blobs(prefix=blob.name)
            file_list = [quote(b.name) for b in blobs if b.name != blob.name]
            tree = Pictures._create_tree(file_list)
            return tree
        else:
            raise InvalidCredentials("Is there any empty credential")

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

    async def upload_files(files: List[UploadFile], file_path: str = ""):
        bucket = client.get_bucket("testes-roque")
        for file in files:
            try:
                blob = bucket.blob(f"{file_path}/{file.filename}")
                blob.upload_from_string(
                    await file.read(), content_type=file.content_type
                )
            except GoogleCloudError as e:
                raise FileUploadError(
                    f"Error sending file {file.filename}: {e}"
                )
        return {"message": "End of upload service"}
