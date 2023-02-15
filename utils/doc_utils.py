import os


def generate_file_name(prefix: str, extension: str) -> str:
    return prefix + "_" + extension


def delete_file(file_path: str, file_name: str) -> None:
    os.remove(file_name)
    os.remove(file_path)
