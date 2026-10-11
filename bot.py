import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    FSInputFile
)
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

TOKEN = "8815598886:AAEf75R27BO_62V_86jm9esLJ1yfG8Q6-3g"

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)
dp = Dispatcher()

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎬 Получить видео"), KeyboardButton(text="📋 Инструкция")],
        [KeyboardButton(text="💬 Поддержка")]
    ],
    resize_keyboard=True
)

async def send_welcome_with_photo(message: types.Message):
    user_name = message.from_user.first_name or "друг"
    
    text = (
        f"Привет, {user_name}! 👋\n\n"
        f"Чтобы получить полное видео **«Два брата и Две сестры»**, выполни 3 простых шага:\n\n"
        f"1️⃣ Зайди в TikTok и вбей в поиск: **«2 брата и 2 сестры»**.\n"
        f"2️⃣ Открой комментарии под видео и скинь в ответ другим людям вот эту картинку "
        f"(она ниже 👇, **такая же стоит у нас на аватарке бота**).\n"
        f"3️⃣ Сделай так 10 раз и отправь нам скриншоты сюда в чат.\n\n"
        f"Как только проверим — сразу откроем доступ к видео!"
    )

    script_dir = os.path.dirname(os.path.abspath(__file__))
    photo_path = os.path.join(script_dir, "pic.jpg")

    if os.path.exists(photo_path):
        photo = FSInputFile(photo_path)
        await message.answer_photo(
            photo=photo,
            caption=text,
            reply_markup=main_menu
        )
    else:
        print(f"⚠️ Картинка не найдена: {photo_path}")
        await message.answer(text, reply_markup=main_menu)

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await send_welcome_with_photo(message)

@dp.message(F.text == "🎬 Получить видео")
async def get_video_handler(message: types.Message):
    await message.answer(
        "⏳ Видео ждёт, пока ты выполнишь все условия!\n"
        "Скинь скриншоты 10 комментариев с картинкой, и мы проверим."
    )

@dp.message(F.text == "📋 Инструкция")
async def get_instruction_handler(message: types.Message):
    await send_welcome_with_photo(message)

@dp.message(F.text == "💬 Поддержка")
async def get_support_handler(message: types.Message):
    await message.answer("Если что-то не получается — пиши сюда, мы на связи!")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
