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
from aiogram.types import Document, ReplyKeyboardMarkup, KeyboardButton
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


async def run_wolphramscript(chat_id: int, file_path: str, namimg: str, state: FSMContext):
    path = Path(file_path)
    work_folder = path.parent
    except_files = [os.path.join(work_folder, x) for x in os.listdir(work_folder)]
    out_file_name = os.path.join(work_folder, "output.txt")
    if os.path.exists(out_file_name):
        os.remove(out_file_name)
    

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
        await state.update_data(process=running_process)
        stdout, stderr = await running_process.communicate()
        
        with open(out_file_name, "w") as out:
            if stdout:
                out.write(str(stdout))
            if stderr:
                out.write(str(stderr))

    else:
        with open(out_file_name, "w") as f:
            f.write("dddd")

    files_after_run = [os.path.join(work_folder, x) for x in os.listdir(work_folder)]

    # WOrk only with decimals
    # files_to_send = set(files_before_run).symmetric_difference(files_after_run)
    # print(files_to_send)
    # for file_name in set(files_before_run) ^ set(files_after_run):
    #     if file_name.endswith(["*jpg", ".png", "*tiff"]):
            
    #     else:
    #         pass

    photos_to_send = []
    documents_to_send = []
    # types.InputMediaPhoto() # for photo
    # types.InputMediaDocument() # for documets
    for file_name in files_after_run:
        if file_name not in except_files:
            if file_name.endswith((".jpg", ".png", ".tiff")):
                photos_to_send.append(types.InputMediaPhoto(type="photo",
                                                            media=types.FSInputFile(file_name)
                                                            )
                                    )
            else:
                documents_to_send.append(types.InputMediaDocument(type="document", 
                                                              media=types.FSInputFile(file_name)
                                                              )
                                    )
    if photos_to_send:
        await bot.send_media_group(chat_id, photos_to_send)
    if documents_to_send:
        await bot.send_media_group(chat_id, documents_to_send)
    if not photos_to_send and not documents_to_send:
        await bot.send_message(chat_id, "Отсутствует вывод программы")
    
    await state.set_state(ProcessingStates.NOTHING)


@dp.message(Command("start"))
async def handle_start(message: types.Message):
    print(message.from_user.id)
    if message.from_user.id in ALLOWED_USERS:
        await message.answer("Файл .wl")


@dp.message(Command("cancel"))
async def cancel_running(message: types.Message, state: FSMContext):
    if message.from_user.id in ALLOWED_USERS:
        if await state.get_state() == ProcessingStates.RUNNING.state:
            data = await state.get_data()
            running_process = data["process"]
            if running_process:
                try:
                    running_process.terminate()
                    await asyncio.sleep(2)
                    if running_process.returncode is None:
                        running_process.kill()
                    await message.answer("Процесс отменён")
                except:
                    await message.answer("Ошибка при отмене процесса")
                finally:
                    await state.set_state(ProcessingStates.NOTHING)
        else:
            await message.answer("Отсутсвуют запущенные скрипты")


@dp.message(F.media_group_id, F.document)
async def handle_media_group(message: types.Message, state: FSMContext):
    if message.from_user.id in ALLOWED_USERS:
        if await state.get_state() == ProcessingStates.RUNNING:
            return await message.answer("отмена /cancel", reply_markup=types.ReplyKeyboardRemove())
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
                keyboard = create_keyboard(wl_files)
                await message.answer(text="Выберите файл для запуска", reply_markup=keyboard)
                await state.set_state(ProcessingStates.CLARIFY)


@dp.message(F.document)
async def handle_document(message: types.Message, state: FSMContext):
    if message.from_user.id in ALLOWED_USERS:
        if await state.get_state() == ProcessingStates.RUNNING.state:
            return await message.answer("отмена /cancel", reply_markup=types.ReplyKeyboardRemove())
        if await state.get_state() == ProcessingStates.CLARIFY.state:
            await state.set_state(ProcessingStates.NOTHING.state, reply_markup=types.ReplyKeyboardRemove())
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
        await state.set_state(ProcessingStates.RUNNING)
        await message.answer("Файл принят в обработку")
        return await run_wolphramscript(message.from_user.id, parsed_filename, now_name, state)
    

@dp.message(ProcessingStates.CLARIFY)
async def clarify_which_file_to_run(message: types.Message, state: FSMContext):
    if message.from_user.id in ALLOWED_USERS:
        message_text = message.text
        data = await state.get_data()
        wl_files: list[str] = data["wl_files"]
        documents: list[Document] = data["documents"]
        if message_text == "Отмена":
            await state.set_state(ProcessingStates.NOTHING.state)
            return await message.answer("Отменено", reply_markup=types.ReplyKeyboardRemove())
        elif message_text not in wl_files:
            return await message.answer("Выберите название файла")
        wl_document = [document for document in documents if document.file_name == message_text][0]
        documents.remove(wl_document)
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
            wl_file = await bot.get_file(document.file_id)
            wl_file_path = wl_file.file_path
            destination = os.path.join(now_folder, document.file_name)
            await bot.download_file(file_path=wl_file_path, destination=destination)
            if document.file_name.endswith(".wl"):
                renamed_destination = os.path.join(now_folder, Path(document.file_name).stem + "_renamed.wl")
                parsed_name = parse_file(destination)
                os.rename(destination, renamed_destination)
                os.rename(parsed_name, destination)
        
        await state.set_state(ProcessingStates.RUNNING)
        await message.answer("Файлы приняты в обработку", reply_markup=types.ReplyKeyboardRemove())
        return await run_wolphramscript(message.from_user.id, parsed_filename, now_name, state)


def create_keyboard(options: list[str], cancel_btn: str = "Отмена") -> ReplyKeyboardMarkup:
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

    keyboard.append([KeyboardButton(text=cancel_btn, callback_data="-1")])
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

asyncio.run(start_polling())