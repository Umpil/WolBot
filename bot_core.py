import aiogram
import asyncio
import os
from pathlib import Path
from utils import *
from decouple import config
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Document
from collections import defaultdict

## mb redis???
media_groups = defaultdict(list)
bot = Bot(token=config("BOT_TOKEN"))
dp = Dispatcher()
DEBUG = config("DEBUG")

ALLOWED_USERS = config("ALLOWED_USERS", cast=lambda v: [int(s.strip()) for s in v.split(',')])
class ProcessingStates(StatesGroup):
    NOTHING = State()
    RUNNING = State()
    CLARIFY = State()


async def start_polling():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, relax=0.1, reset_webhook=True)

async def run_wolphramscript(chat_id: int, file_path: str, namimg: str):
    path = Path(file_path)
    work_folder = path.parent
    except_files = [os.path.join(work_folder, namimg + ".wl"), file_path]
    out_file_name = os.path.join(work_folder, "output.txt")
    
    # with open(out_file_name, "w") as f:
    #     f.write("dddd")

    with open(os.path.join(work_folder, "test.txt"), "w") as f:
        f.write("test")

    if not DEBUG:
        running_process = await asyncio.create_subprocess_exec(
            "wolframscript",
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

@dp.message(Command("cancel"))
async def cancel_running(message: types.Message):
    print("ADD CANCEL")

@dp.message(F.media_group_id, F.document)
async def handle_media_group(message: types.Message, state: FSMContext):
    media_group_id = message.media_group_id
    media_groups[media_group_id].append(message.document)
    
    await asyncio.sleep(1)  # Костыль
    
    if media_group_id in media_groups:
        documents: list[Document]  = media_groups.pop(media_group_id)
        check_list = [document.file_name.endswith(".wl") for document in documents]
        how_many_wl_files = sum(check_list)
        if not how_many_wl_files:
            await message.answer("No wl")
            return
        elif how_many_wl_files == 1:
            try:
                wl_index = check_list.index(True)
                wl_document = documents.pop(wl_index)
                wl_file = await bot.get_file(wl_document.file_id)
                wl_file_path = wl_file.file_path
                user_folder = hash_user_id(message.from_user.id)
                now_name = Path(wl_document.file_name).stem
                now_folder = os.path.join(media_folder, user_folder, now_name)
                if not os.path.exists(now_folder):
                    os.makedirs(now_folder, exist_ok=True)
                destination = os.path.join(now_folder, wl_document.file_name)
                await bot.download_file(file_path=wl_file_path, destination=destination)
                parsed_filename = parse_file(destination)
                for document in documents:
                    # File size ???
                    file = await bot.get_file(document.file_id)
                    file_path = file.file_path
                    destination = os.path.join(now_folder, document.file_name)
                    await bot.download_file(file_path=file_path, destination=destination)
                await state.set_state(ProcessingStates.RUNNING)
                await message.answer("Файлы приняты в обработку")
                return await run_wolphramscript(message.from_user.id, parsed_filename, now_name)
            except ValueError:
                return await message.answer("Internal error")
        else:
            wl_files = [document.file_name for document, flag in zip(documents, check_list) if flag]
            await state.update_data(documents=documents, wl_files=wl_files)
    
            await state.set_state(ProcessingStates.CLARIFY)

@dp.message(ProcessingStates.CLARIFY)
def clarify_which_file_to_run(message: types.Message, state: FSMContext):
    pass

@dp.message(F.document)
async def handle_document(message: types.Message, state: FSMContext):
    if message.from_user.id in ALLOWED_USERS:
        if await state.get_state() == ProcessingStates.RUNNING.state:
            return await message.answer("отмена /cancel")
        document = message.document
        await message.answer(f"Файл {document.file_name}")
        file_name = document.file_name
        if not file_name.endswith(".wl"): 
            return await message.answer("Bad wl")
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
        return await run_wolphramscript(message.from_user.id, parsed_filename, now_name)
        

asyncio.run(start_polling())