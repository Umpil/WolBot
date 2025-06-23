import aiogram
import cv2
import asyncio
import os
from pathlib import Path
from utils import *
from decouple import config
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, Filter

bot = Bot(token=config("BOT_TOKEN"))
dp = Dispatcher()

class CustomFilter(Filter):
    def __init__(self):
        super().__init__()

    def __call__(self, *args, **kwds):
        return super().__call__(*args, **kwds)

ALLOWED_USERS = config("ALLOWED_USERS", cast=lambda v: [int(s.strip()) for s in v.split(',')])
class ProcessingStates(StatesGroup):
    WAITING_EXECUTION = State()
    WAITING_SEND = State()


async def start_polling():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, relax=0.1, reset_webhook=True)

async def run_wolphramscript(chat_id: int, file_path: str, namimg: str):
    work_folder = "\\".join(file_path.split("\\")[0: -1])
    except_files = [os.path.join(work_folder, namimg + ".wl"), file_path]
    out_file_name = os.path.join(work_folder, "output.txt")
    
    with open(out_file_name, "w") as f:
        f.write("dddd")

    with open(os.path.join(work_folder, "test.txt"), "w") as f:
        f.write("test")

    running_process = await asyncio.create_subprocess_exec(
        "wolphramscript",
        "-f",
        file_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await running_process.communicate()
    
    with open(out_file_name, "w") as out:
        if stdout:
            out.write(str(stdout))
        if stderr:
            out.write(str(stderr))

    files_after_run = [os.path.join(work_folder, x) for x in os.listdir(work_folder)]

    # WOrk only with decimals
    # files_to_send = set(files_before_run).symmetric_difference(files_after_run)
    # print(files_to_send)
    # for file_name in set(files_before_run) ^ set(files_after_run):
    #     if file_name.endswith(["*jpg", ".png", "*tiff"]):
            
    #     else:
    #         pass

    files_to_send = []
    # types.InputMediaPhoto() # for photo
    # types.InputMediaDocument() # for documets
    for file_name in files_after_run:
        if file_name not in except_files:
            if file_name.endswith(("*jpg", ".png", "*tiff")):
                files_to_send.append(types.InputMediaPhoto(type="photo",
                                                            media=types.FSInputFile(file_name)
                                                            )
                                    )
            else:
                files_to_send.append(types.InputMediaDocument(type="document", 
                                                              media=types.FSInputFile(file_name)
                                                              )
                                    )
    if files_to_send:
        await bot.send_media_group(chat_id, list(files_to_send))
    else:
        await bot.send_message(chat_id, "Отсутсвует вывод программы")


@dp.message(Command("start"))
async def handle_start(message: types.Message):
    print(message.from_user.id)
    if message.from_user.id in ALLOWED_USERS:
        await message.answer("Файл .wl")

@dp.message(aiogram.F.document)
async def handle_document(message: types.Message, state: FSMContext):
    if message.from_user.id in ALLOWED_USERS:
        document = message.document
        file_name = document.file_name
        if not file_name.endswith(".wl"): 
            await message.answer("Bad wl")
            return
        file_id = document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        user_folder = hash_user_id(message.from_user.id)
        now_name = Path(file_name).stem
        now_folder = os.path.join(media_folder, user_folder, now_name)
        if not os.path.exists(now_folder):
            os.makedirs(now_folder, exist_ok=True)
        destination = os.path.join(now_folder, file_name)
        await bot.download_file(file_path=file_path, destination=destination)
        parsed_filename = parse_file(destination)
        await state.set_state(ProcessingStates.WAITING_EXECUTION)
        await message.answer("Файл принят в обработку")
        await run_wolphramscript(message.from_user.id, parsed_filename, now_name)
        

asyncio.run(start_polling())