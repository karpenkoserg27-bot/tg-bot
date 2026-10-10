import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiohttp import web

# Инициализация бота с твоим токеном
TOKEN = "8815598886:AAEf75R27BO_62V_86jm9esLJ1yfG8Q6-3g"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Клавиатура
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎬 Получить видео")],
        [KeyboardButton(text="📜 Инструкция"), KeyboardButton(text="💬 Поддержка")]
    ],
    resize_keyboard=True
)

# Функция записи пользователя в файл
def register_user(user_id: int):
    users_file = "users.txt"
    if not os.path.exists(users_file):
        open(users_file, "w").close()
    
    with open(users_file, "r") as f:
        users = f.read().splitlines()
        
    if str(user_id) not in users:
        with open(users_file, "a") as f:
            f.write(str(user_id) + "\n")

# Обработка команды /start
@dp.message(Command("start"))
async def command_start_handler(message: types.Message):
    register_user(message.from_user.id)
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋 Чтобы получить полное видео «Два брата и Две сестры», выполни 3 простых шага:\n\n"
        "1️⃣ Зайди в TikTok и вбей в поиск: «2 брата и 2 сестры».\n"
        "2️⃣ Открой комментарии под видео и скинь в ответ другим людям вот эту картинку (она ниже 👇, такая же стоит у нас на аватарке бота).\n"
        "3️⃣ Сделай так 10 раз и отправь нам скриншоты сюда в чат.\n\n"
        "Как только проверим — сразу откроем доступ к видео!",
        reply_markup=keyboard
    )

# Команда для тебя — смотреть статистику (/stats)
@dp.message(Command("stats"))
async def stats_handler(message: types.Message):
    users_file = "users.txt"
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            count = len(f.read().splitlines())
    else:
        count = 0
    await message.answer(f"📊 Всего пользователей в боте: {count} чел.")

# Кнопка Инструкция
@dp.message(F.text == "📜 Инструкция")
async def get_instruction_handler(message: types.Message):
    await message.answer(
        "📜 **Инструкция по выполнению:**\n\n"
        "1. Зайди в TikTok и найди видео «2 брата и 2 сестры».\n"
        "2. Оставь комментарии с нашей картинкой под видео.\n"
        "3. Сделай 10 скриншотов и отправь их прямо сюда в бот!",
        reply_markup=keyboard
    )

# Кнопка Получить видео
@dp.message(F.text == "🎬 Получить видео")
async def get_video_handler(message: types.Message):
    await message.answer("Отправь сюда 10 скриншотов с подтверждением, и мы сразу пришлем доступ!")

# Кнопка Поддержка
@dp.message(F.text == "💬 Поддержка")
async def support_handler(message: types.Message):
    await message.answer("Если есть вопросы — напиши автору бота.")

# Веб-сервер для поддержания работы на Render
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

async def main():
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
