from pathlib import Path
import os
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
HELLO_WORD = '''
Данный бот позволяет запускать вольфрам скрипты.\n
Поддерживаемый формат ".wl", допускается загрузка дополнительных файлов для работы скрипта.\n
Возможен запуск только 1-го скрипта, для отмены запущенного скрипта используйте команду /cancel\n
'''
media_folder = "UserFiles"

def parse_file(filename: str, out_filename=None) -> str:
    if not out_filename:
        path = Path(filename)
        out_filename = str(path.parent / (path.stem + "_parsed.wl"))
    with open(filename, "r") as file:
        file_lines = file.readlines()

    with open(out_filename, "w") as file:
        skip_mode = False 
        prev_line_empty = False  
        
        for line in file_lines:
            if line.startswith("(* ::Text:: *)"):
                skip_mode = True
                continue

            if skip_mode and line == "\n":
                if prev_line_empty:
                    skip_mode = False 
                    prev_line_empty = False
                    continue
                prev_line_empty = True
                continue

            if not skip_mode and line not in ("(* ::Input:: *)\n", "(* ::Package:: *)\n"):
                if line.startswith("(*") and line.endswith("*)\n"):
                    file.write(line[2:-3] + "\n")
                else:
                    file.write(line)

            prev_line_empty = (line == "\n")

    return out_filename

def create_keyboard(options: list[str]) -> ReplyKeyboardMarkup:
    keyboard = []
    row = []
    callback_data = 0
    for option in options:
        row.append(KeyboardButton(text=option, callback_data=str(callback_data)))
        if len(row) == 2:
            keyboard.append(row)
            row = []
        callback_data += 1
    
    if row:
        keyboard.append(row)

    keyboard.append([KeyboardButton(text="Отмена", callback_data="-1")])
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def hash_user_id(user_id: int | str):
    return str(user_id)