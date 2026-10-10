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

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Выбери нужный раздел в меню ниже:", reply_markup=keyboard)

@dp.message(F.text == "🎬 Получить видео")
async def get_video_handler(message: types.Message):
    await message.answer(
        "⏳ Видео ждет, пока ты выполнишь все условия!\n"
        "Скинь скриншоты 10 комментариев с картинкой, и мы проверим."
    )

@dp.message(F.text == "📜 Инструкция")
async def get_instruction_handler(message: types.Message):
    await message.answer(""📜 **Инструкция по выполнению:**\n\n"
        "1. Зайди в TikTok и найди нужное видео.\n"
        "2. Оставь комментарий и прикрепи картинку.\n"
        "3. Повтори 10 раз и отправь скриншоты сюда!", reply_markup=keyboard)

@dp.message(F.text == "💬 Поддержка")
async def get_support_handler(message: types.Message):
    await message.answer("Если что-то не получается, пиши сюда, мы на связи!")

# Фиктивный веб-сервер для успешной проверки Render
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    print("Бот и веб-сервер запущены...")
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
