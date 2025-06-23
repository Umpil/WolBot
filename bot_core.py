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
        

asyncio.run(start_polling())