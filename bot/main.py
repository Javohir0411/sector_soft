import os
import sys

# Loyihaning ildizini sys.path ga qo‘shamiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # C:\sector_soft

# Django muhitini sozlash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()
from bot.handlers import register, start, delete_user
from aiogram import Bot, Dispatcher
from bot.configuration import BOT_TOKEN
import asyncio



async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Routerlar ulanishi
    dp.include_router(start.command_router)
    dp.include_router(register.router)
    dp.include_router(delete_user.router)

    print("Bot ishga tushdi...")  # konsolga yoziladi
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
