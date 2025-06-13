from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from asgiref.sync import sync_to_async
from app_store.models import BotUser

router = Router()

@router.message(Command("delete"))
async def delete_user_handler(message: Message, state: FSMContext):
    await state.clear()
    telegram_id = message.from_user.id

    # Foydalanuvchining tilini aniqlaymiz
    user = await sync_to_async(lambda: BotUser.objects.filter(telegram_id=telegram_id).first())()
    lang = getattr(user, "lang", "uz")  # topilmasa — "uz"

    deleted_count, _ = await sync_to_async(
        BotUser.objects.filter(telegram_id=telegram_id).delete
    )()

    responses = {
        "uz": {
            "deleted": "🗑️ Ma'lumotlaringiz bazadan o'chirildi.",
            "not_found": "🚫 Siz ro'yxatdan o'tmagansiz yoki ma'lumot topilmadi."
        },
        "ru": {
            "deleted": "🗑️ Ваши данные были удалены из базы.",
            "not_found": "🚫 Вы не зарегистрированы или данные не найдены."
        }
    }

    msg = responses[lang]["deleted"] if deleted_count else responses[lang]["not_found"]
    await message.answer(msg)

