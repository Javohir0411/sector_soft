from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from asgiref.sync import sync_to_async
from app_store.models import Product, ProductColor, ProductImage
from bot.keyboards.get_categories_and_products import get_user_lang
from django.conf import settings  # ✅ BASE_URL olish uchun
from aiogram.types import FSInputFile

router = Router()

@sync_to_async
def get_product_by_id(product_id):
    return Product.objects.get(id=product_id)

@sync_to_async
def get_colors(product):
    return list(product.colors.all())

@router.callback_query(F.data.startswith("product_"))
async def show_product_colors(callback: CallbackQuery):
    await callback.answer()
    product_id = int(callback.data.split("_")[1])
    telegram_id = callback.from_user.id
    lang = await get_user_lang(telegram_id)

    product = await get_product_by_id(product_id)
    colors = await get_colors(product)

    if not colors:
        text = "Ushbu mahsulotda ranglar mavjud emas." if lang == "uz" else "Для этого товара нет цветов."
        await callback.message.answer(text)
        return

    keyboard = [
        [InlineKeyboardButton(
            text=f"{getattr(color, f'product_color_{lang}')} - {color.price} {color.currency}",
            callback_data=f"color_{color.id}"
        )]
        for color in colors
    ]

    text = "Rangni tanlang:" if lang == "uz" else "Выберите цвет:"
    await callback.message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))


@sync_to_async
def get_color_by_id(color_id):
    return ProductColor.objects.select_related("product").get(id=color_id)

@router.callback_query(F.data.startswith("color_"))
async def show_product_detail_by_color(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    color_id = int(callback.data.split("_")[1])
    color = await get_color_by_id(color_id)
    product = color.product

    lang = await get_user_lang(callback.from_user.id)
    name = getattr(product, f"product_name_{lang}")
    description = getattr(product, f"product_descriptions_{lang}")
    caption = f"<b>{name}</b>\n\n{description}"

    images = await sync_to_async(list)(color.images.all())

    if images:
        for img in images:
            if img.image:
                file_path = img.image.path  # local path
                try:
                    photo = FSInputFile(file_path)
                    await callback.message.answer_photo(photo=photo)
                except Exception as e:
                    print("❌ Telegramga yuborilmadi:", e)
    else:
        await callback.message.answer("Rasmlar mavjud emas." if lang == "uz" else "Изображения отсутствуют.")

    await callback.message.answer(text=caption, parse_mode="HTML")
