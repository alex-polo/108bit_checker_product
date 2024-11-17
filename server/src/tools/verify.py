import os

from fastapi import HTTPException


def is_file_exist(file_path: str):
    if file_path is None or not os.path.isfile(file_path):
        return False
    else:
        return True