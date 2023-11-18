from secrets import token_hex
import os
from fastapi import UploadFile, File


def file_or_image_upload(folder_dir:str, file: UploadFile = File(...)):
    file_random_name = token_hex(30)
    file_ext = file.filename.split('.')[-1]
    file_save_path = f'./uploads/{folder_dir}/{file_random_name}.{file_ext}'

    # ? it will create the directory dynamically
    os.makedirs(os.path.dirname(file_save_path), exist_ok=True)

    with open(file_save_path, 'wb') as f:
        content = file.file.read()
        f.write(content)
    file_path = f"{folder_dir}/{file_random_name}.{file_ext}"
    return file_path
