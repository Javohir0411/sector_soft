import sys
import os
import django

# Loyihaning ildiz papkasini sys.path ga qo‘shamiz
sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from app_store.models import Category
from app_store.serializers import CategoryGetSerializer

# Botni sozlash
bot = Bot(
    token="8006601858:AAH4_-HfzIUV_ISzjhcYTXqxXjlmsLGCWfo",
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

@dp.message()
async def list_categories(message: Message):
    lang = "en" if message.from_user.language_code == "en" else "uz"
    categories = Category.objects.all()
    serializer = CategoryGetSerializer(categories, many=True, context={"lang": lang})
    data = serializer.data

    response = "📂 Categories:\n"
    for category in data:
        response += f"— {category['category_name']}\n"

    await message.answer(response)

if __name__ == "__main__":
    import asyncio
    from aiogram import Dispatcher

    async def main():
        await dp.start_polling(bot)

    asyncio.run(main())
