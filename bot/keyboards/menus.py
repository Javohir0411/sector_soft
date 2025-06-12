from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="/start")], KeyboardButton(text="/delete")],
    resize_keyboard=True
)
