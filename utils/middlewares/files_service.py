import io
import os
import zipfile
from typing import List
from urllib.parse import unquote
from fastapi import UploadFile
from urllib.parse import quote
from datetime import timedelta


async def extract_files(files: List[UploadFile]) -> List[UploadFile]:
    extracted_files = []
    for file in files:
        if file.filename.endswith(".zip"):
            zip_data = io.BytesIO(await file.read())
            with zipfile.ZipFile(zip_data) as myzip:
                folder_name = os.path.splitext(file.filename)[0]
                for zip_file in myzip.infolist():
                    file_data = myzip.read(zip_file.filename)
                    extracted_file = UploadFile(
                        file=io.BytesIO(file_data),
                        filename=f"{folder_name}/{zip_file.filename}",
                    )
                    extracted_files.append(extracted_file)
        else:
            extracted_files.append(file)
    return extracted_files


def generate_preview_url(blob):
    extension = os.path.splitext(blob.name)[1].lower()

    if extension in ['.jpg', '.jpeg', '.png', '.gif']:
        return blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=5),
            method="GET",
        )
    else:
        return None


def create_tree(file_list: list, root_path: str, prefix: str):
    root = []
    node_dict = {}
    root_parts = root_path.split("/")
    for blob in file_list:
        path = quote(blob.name.replace(prefix, "", 1))
        preview_url = generate_preview_url(blob)

        current_node = root
        parts = path.split("/")
        for i, part in enumerate(parts):
            if not part or (i < len(root_parts) and part == root_parts[i]):
                continue
            full_path = "/".join(parts[: i + 1])
            if full_path not in node_dict:
                node = {
                    "title": unquote(part),
                    "content": [] if i != len(parts) - 1 else [],
                    "preview_url": preview_url
                }
                node_dict[full_path] = node
                current_node.append(node)
            current_node = node_dict[full_path]["content"]
            if isinstance(current_node, dict):
                break
    return root


def get_new_name(name: str, count: int) -> str:
    base, ext = os.path.splitext(name)
    if base.endswith(f" ({count-1})"):
        new_base = base[: base.rfind(f" ({count-1})")]
        new_name = f"{new_base} ({count}){ext}"
    else:
        new_name = f"{base} ({count}){ext}"
    return new_name
