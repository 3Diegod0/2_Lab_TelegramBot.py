import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import os
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO)

load_dotenv()

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()

random_number = random.randint(1, 100)
attempts = 0

@dp.message(Command('start'))
async def start(message: types.Message):
    global random_number, attempts
    random_number = random.randint(1, 100)
    attempts = 0
    await message.answer("Привет! Я загадал число от 1 до 100. Попробуй угадать!")

@dp.message()
async def guess_number(message: types.Message):
    global random_number, attempts
    user_number = int(message.text)
    attempts += 1

    if user_number == random_number:
        await message.answer(f"Поздравляю, вы угадали число за {attempts} попыток!")
    elif user_number < random_number:
        await message.answer("Загаданное число больше. Попробуйте еще раз!")
    else:
        await message.answer("Загаданное число меньше. Попробуйте еще раз!")

async def main():
    await  bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling((bot))