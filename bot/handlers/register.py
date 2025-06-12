# from aiogram import Router, F
# from aiogram.types import Message, ReplyKeyboardRemove
# from asgiref.sync import sync_to_async
# from app_store.models import BotUser
#
# router = Router()
#
# @router.message(F.contact)
# async def contact_handlers(message: Message):
#     contact = message.contact
#
#     if not contact:
#         await message.answer("Iltimos tugma orqali telefon raqam yuboring!")
#         return
#
#     if contact.user_id != message.from_user.id:
#         await message.answer("Iltimos, faqat o'z raqamingizni yuboring.")
#         return
#
#     # full_name to‘g‘ri aniqlanmoqda
#     full_name = f"{contact.first_name or ''} {contact.last_name or ''}".strip()
#
#     await sync_to_async(BotUser.objects.get_or_create)(
#         telegram_id=message.from_user.id,
#         defaults={
#             "full_name": full_name,
#             "phone_number": contact.phone_number
#         }
#     )
#
#     await message.answer(
#         "Siz muvaffaqiyatli ro'yxatga olindingiz ✅",
#         reply_markup=ReplyKeyboardRemove()
#     )

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

from app_store.models import BotUser

router = Router()

class RegisterStates(StatesGroup):
    full_name = State() #  foydalanuvchi ism-familiyasini yozadigan bosqich.


@router.message(F.contact)
async def contact_handler(message: Message, state: FSMContext):
    contact = message.contact

    if not contact or contact.user_id != message.from_user.id:
        await message.answer("Iltimos, faqat o'z raqamingizni tugma orqali yuboring!")
        return

    await state.update_data(phone_number=contact.phone_number, telegram_id=message.from_user.id)
    await message.answer("Endi ismingiz va familiyangizni kiriting:")
    await state.set_state(RegisterStates.full_name)


@router.message(RegisterStates.full_name)
async def get_full_name(message: Message, state: FSMContext):
    data = await state.get_data()
    full_name = message.text.strip()
    telegram_id = data.get("telegram_id")
    phone_number = data.get("phone_number")

    await sync_to_async(BotUser.objects.get_or_create)(
        telegram_id=telegram_id,
        defaults={
            "full_name": full_name,
            "phone_number": phone_number
        }
    )

    await state.clear()
    await message.answer("✅ Siz muvaffaqiyatli ro'yxatdan o'tdingiz.", reply_markup=ReplyKeyboardRemove())
