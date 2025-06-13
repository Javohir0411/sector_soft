from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from asgiref.sync import sync_to_async

from app_store.models import BotUser
from aiogram.filters import CommandStart


router = Router()


class StartStates(StatesGroup):
    choose_language = State()
    waiting_contact = State()
    waiting_name = State()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    # botni ishga tushirganida birinchi bo'lib, kerakli tilni tanlab olamiz!

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🇺🇿 Uzbek")], [KeyboardButton(text="🇷🇺 Russian")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Iltimos, tilni tanlang:\nПожалуйста, выберите язык:", reply_markup=keyboard)
    await state.set_state(StartStates.choose_language)


@router.message(StartStates.choose_language)
async def choose_language(message: Message, state: FSMContext):
    text = message.text.lower()
    if "uzbek" in text or "uz" in text:
        lang = "uz"
    elif "russian" in text or "ru" in text:
        lang = "ru"
    else:
        await message.answer("Iltimos, tugmalardan birini tanglang !")
        return

    await state.update_data(lang=lang)
    await state.set_state(StartStates.waiting_contact)

    button_text = {
        "uz": "📱 Telefon raqam yuborish",
        "ru": "📱 Отправить номер телефона"
    }

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=button_text[lang], request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    text = {
        "uz": "Iltimos, telefon raqamingizni yuboring:",
        "ru": "Пожалуйста, отправьте свой номер телефона:"
    }

    await message.answer(text[lang], reply_markup=keyboard)
    await state.set_state(StartStates.waiting_contact)


@router.message(StartStates.waiting_contact, F.contact)
async def get_contact(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    text = {
        "uz": "Iltimos, tugma orqali o'z raqamingizni yuboring!",
        "ru": "Пожалуйста, отправьте свой номер с помощью кнопки."
    }
    contact = message.contact
    if not contact or contact.user_id != message.from_user.id:
        await message.answer(text[lang])
        return

    telegram_id = message.from_user.id
    user_exists = await sync_to_async(BotUser.objects.filter(telegram_id=telegram_id).exists)()

    if user_exists:
        text = {
            "uz": "Siz avval ro'yxatdan o'tgansiz...",
            "ru": "Вы уже зарегистрированы..."
        }
        await message.answer(text[lang])
        await state.clear()
        return

    text = {
        "uz": "Endi, ismingiz va familiyangizni kiriting...",
        "ru": "Теперь введите свое имя и фамилию..."
    }

    await state.update_data(phone_number=contact.phone_number, telegram_id=telegram_id)
    await message.answer(text[lang], reply_markup=ReplyKeyboardRemove())
    await state.set_state(StartStates.waiting_name)


@router.message(StartStates.waiting_name)
async def get_full_name(message: Message, state: FSMContext):
    data = await state.get_data()
    full_name = message.text.strip()
    telegram_id = data.get("telegram_id")
    phone_number = data.get("phone_number")
    lang = data.get("lang", "uz")

    user, created = await sync_to_async(BotUser.objects.get_or_create)(
        telegram_id=telegram_id,
        defaults={
            "full_name": full_name,
            "phone_number": phone_number,
            "lang": lang
        }
    )
    if created:
        print(f"✅ Foydalanuvchi {user} yaratildi")
    else:
        print(f"ℹ️ {user} Foydalanuvchi avvaldan mavjud")

    text = {
        "uz": f"✅ <b>{full_name}</b>, siz muvaffaqiyatli ro'yxatdan o'tdingiz.",
        "ru": f"✅ <b>{full_name}</b>, вы успешно зарегистрировались."
    }


    await message.answer(text[lang])
    await state.clear()
