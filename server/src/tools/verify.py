import os

from fastapi import HTTPException


def file_exist_exception(file_path: str):
    if file_path is None or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")