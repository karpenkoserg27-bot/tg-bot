import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton,
    FSInputFile
)

# Токен твоего бота
TOKEN = "8815598886:AAEf75R27BO_62V_86jm9esLJ1yfG8Q6-3g"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Главное меню с кнопками
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎬 Получить видео"), KeyboardButton(text="📋 Инструкция")],
        [KeyboardButton(text="💬 Поддержка")]
    ],
    resize_keyboard=True
)

async def send_welcome_with_photo(message: types.Message):
    user_name = message.from_user.first_name
    text = (
        f"Привет, {user_name}! 👋 Чтобы получить полное видео **«Два брата и Две сестры»**, выполни 3 простых шага:\n\n"
        f"1️⃣ Зайди в TikTok и вбей в поиск: **«2 брата и 2 сестры»**.\n"
        f"2️⃣ Открой комментарии под видео и скинь в ответ другим людям вот эту картинку (она ниже 👇, **такая же стоит у нас на аватарке бота**).\n"
        f"3️⃣ Сделай так 10 раз и отправь нам скриншоты сюда в чат.\n\n"
        f"Как только проверим — сразу откроем доступ к видео!"
    )
    
    # Автоматически определяем путь к папе с скриптом и ищем pic.jpg рядом
    script_dir = os.path.dirname(os.path.abspath(__file__))
    photo_path = os.path.join(script_dir, "pic.jpg")
    
    if os.path.exists(photo_path):
        photo = FSInputFile(photo_path)
        await message.answer_photo(
            photo=photo, 
            caption=text, 
            parse_mode="Markdown", 
            reply_markup=main_menu
        )
    else:
        print(f"⚠️ Картинка не найдена по пути: {photo_path}")
        await message.answer(text, parse_mode="Markdown", reply_markup=main_menu)

# Запуск по команде /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await send_welcome_with_photo(message)

# Кнопка: 🎬 Получить видео
@dp.message(F.text == "🎬 Получить видео")
async def get_video_handler(message: types.Message):
    await message.answer(
        "⏳ Видео ждет, пока ты выполнишь все условия!\n"
        "Скинь скриншоты 10 комментариев с картинкой, и мы проверим."
    )

# Кнопка: 📋 Инструкция
@dp.message(F.text == "📋 Инструкция")
async def get_instruction_handler(message: types.Message):
    await send_welcome_with_photo(message)

# Кнопка: 💬 Поддержка
@dp.message(F.text == "💬 Поддержка")
async def get_support_handler(message: types.Message):
    await message.answer("Если что-то не получается, пиши сюда, мы на связи!")

async def main():
    print("Бот запущен и готов помогать...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())