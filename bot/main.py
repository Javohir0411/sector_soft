from aiogram.client.default import DefaultBotProperties
import logging
import asyncio
import sys
import os

from aiogram.types import BotCommand

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Django sozlamalarini yuklash
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # loyihaning ildizini sys.path ga qo'shamiz
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

django.setup()

# Aiogram modullarini chaqirish
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

#  FSM uchun xotira (storage)
from aiogram.fsm.storage.memory import MemoryStorage

#  Token va handlerlar
from configuration import BOT_TOKEN
from bot.handlers import start
from bot.handlers import delete_user as delete_user_router
from bot.keyboards import get_categories_and_products
from bot.keyboards.get_product_details import router as product_details_router


async def main():
    #  Bot va dispatcher
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    #  Routerlarni ulash
    dp.include_router(start.router)
    dp.include_router(delete_user_router.router)
    dp.include_router(get_categories_and_products.router)
    dp.include_router(product_details_router)

    # O'zbekcha
    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Botni ishga tushirish"),
            BotCommand(command="delete", description="Ma'lumotlaringizni o'chirish"),
            BotCommand(command="category", description="Do'kon mahsulotlarini kategoriyalarini ko'rish")
        ],
        language_code="uz"
    )

    # Русский
    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Запустить бота"),
            BotCommand(command="delete", description="Удалить ваши данные"),
            BotCommand(command="category", description="Просмотр категорий товаров магазина")
        ],
        language_code="ru"
    )

    # Default (fallback, agar til aniqlanmasa)
    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Start the bot"),
            BotCommand(command="delete", description="Delete your data"),
            BotCommand(command="category", description="View store product categories")
        ]
    )

    print("Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot Stopped')
