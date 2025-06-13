from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from app_store.models import Cart, CartItem, BotUser, ProductColor
from bot.keyboards.utils import get_user_lang

router = Router()

@sync_to_async
def get_or_create_cart(user_id):
    user, _ = BotUser.objects.get_or_create(telegram_id=user_id)
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart

@sync_to_async
def add_to_cart(cart, color_id):
    product_color = ProductColor.objects.get(id=color_id)
    item, created = CartItem.objects.get_or_create(cart=cart, product_color=product_color)
    if not created:
        item.quantity += 1
        item.save()

@router.callback_query(F.data.startswith("addtocart_"))
async def add_to_cart_handler(callback: CallbackQuery):
    await callback.answer()
    color_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    cart = await get_or_create_cart(user_id)
    await add_to_cart(cart, color_id)

    lang = await get_user_lang(user_id)
    msg = "Savatchaga qo‘shildi ✅" if lang == "uz" else "Добавлено в корзину ✅"
    await callback.message.answer(msg)

def get_add_to_cart_button(color_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛒 Savatchaga qo‘shish",
                    callback_data=f"addtocart_{color_id}"
                )
            ]
        ]
    )
