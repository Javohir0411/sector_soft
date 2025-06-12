from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from asgiref.sync import sync_to_async

from app_store.models import BotUser
from aiogram.filters import CommandStart

command_router = Router()


@command_router.message(CommandStart())
async def start_handler(message: Message):
    telegram_id = message.from_user.id

    user_exists = await sync_to_async(
        BotUser.objects.filter(telegram_id=telegram_id).exists
    )()

    if user_exists:
        await message.answer("Siz avval ro'yxatdan o'tgansiz...")
        return

    # Telefon raqam so'rash
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📱 Telefon raqam yuborish", request_contact=True)]
    ],
        resize_keyboard=True,  # chiqadigan klaviaturani ekran hajmiga moslab beradi
        one_time_keyboard=True  # Klaviatura bir marotaba chiqadi
    )
    await message.answer("Iltimos telefon raqam yuboring: ", reply_markup=keyboard)
