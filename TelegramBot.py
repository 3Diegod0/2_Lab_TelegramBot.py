import logging
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)
TOKEN = "7095651321:AAGMwvocGc3g_tc3vxHtVQ3bKYeovDsgkIA"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Начальное состояние игры
game_state = {
    "number": None,
    "attempts": 0,
    "min_value": 1,
    "max_value": 100
}

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if len(message.text.split()) > 1:
        try:
            number = int(message.text.split()[1])
            if number < game_state["min_value"] or number > game_state["max_value"]:
                await message.reply(f"Пожалуйста, загадай число в диапазоне от {game_state['min_value']} до {game_state['max_value']}.")
                return
            game_state["number"] = number
            await message.reply("Отлично! Я начинаю угадывать.")
            await ask_question(message)
        except ValueError:
            await message.reply("Пожалуйста, загадай целое число после команды /start.")
    else:
        await message.reply("Пожалуйста, загадай число после команды /start, например: /start 42")

# Обработчик ответов на вопросы
@dp.message_handler()
async def handle_answer(message: types.Message):
    if game_state["number"] is None:
        return

    answer = message.text.lower()

    if answer == "больше":
        if game_state["guess"] < game_state["number"]:
            game_state["min_value"] = game_state["guess"] + 1
        else:
            await message.reply("Не пытайся меня обмануть! Я уже угадал число.")
            return
    elif answer == "меньше":
        if game_state["guess"] > game_state["number"]:
            game_state["max_value"] = game_state["guess"] - 1
        else:
            await message.reply("Не пытайся меня обмануть! Я уже угадал число.")
            return
    elif answer == "угадал":
        await message.reply(f"Ура! Я угадал число {game_state['guess']} за {game_state['attempts']} попыток.")
        game_state["number"] = None
        game_state["attempts"] = 0
        game_state["min_value"] = 1
        game_state["max_value"] = 100
        return
    else:
        await message.reply("Пожалуйста, ответьте 'больше', 'меньше' или 'угадал'.")
        return

    game_state["attempts"] += 1
    await ask_question(message)

async def ask_question(message: types.Message):
    game_state["guess"] = (game_state["min_value"] + game_state["max_value"]) // 2
    await message.reply(f"Мое предположение: {game_state['guess']}. Загаданное число больше, меньше или я угадал?")

async def main():
    await  bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling((bot))
