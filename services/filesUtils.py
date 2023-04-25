import asyncio
import os
import subprocess
import logging

def convert_to_wav(file_path):
    output_file_path = file_path.split('.')[0] + '_converted.wav'

    command = f'ffmpeg -i {file_path} -ac 1 -ar 16000 {output_file_path}'
    subprocess.run(command, shell=True, check=True)

    return output_file_path

def unique_filename(file: str, path: str) -> str:
    """Change file name if file already exists"""
    # check if file exists
    if not os.path.exists(os.path.join(path, file)):
        return file
    # get file name and extension
    filename, filext = os.path.splitext(file)
    # get full file path without extension only
    filexx = os.path.join(path, filename)
    # create incrementing variable
    i = 1
    # determine incremented filename
    while os.path.exists(f'{filexx}_{str(i)}{filext}'):
        # update the incrementing variable
        i += 1
    return f'{filename}_{str(i)}{filext}'

async def delete_file(file_path: str) -> None:
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, os.remove, file_path)
        logging.info(f"Файл {file_path} успешно удален")
    except FileNotFoundError:
        logging.info(f"Файл {file_path} не найден")
    except OSError as e:
        logging.info(f"Ошибка удаления файла {file_path}: {e}")