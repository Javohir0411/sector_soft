from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from asgiref.sync import sync_to_async
from app_store.models import BotUser

router = Router()


@router.message(F.text.lower() == "delete")
async def delete_user_handler(message: Message):
    telegram_id = message.from_user.id

    deleted_count = await sync_to_async(BotUser.objects.filter(telegram_id=telegram_id).delete)()

    if deleted_count:
        await message.answer("Ma'lumotlaringiz bazadan o'chirildi 🗑️")
    else:
        await message.answer("Siz ro'yxatdan o'tmagansiz yoki ma'lumotlar topilmadi.")
