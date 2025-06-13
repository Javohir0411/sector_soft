# from aiogram import Router, F
# from aiogram.fsm.context import FSMContext
# from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
# from asgiref.sync import sync_to_async
# from app_store.models import Product, ProductColor, ProductImage
# from django.conf import settings  # ✅ BASE_URL olish uchun
# from aiogram.types import FSInputFile
# from aiogram.utils.markdown import hbold
#
# from bot.keyboards.get_categories_and_products import get_user_lang
#
# router = Router()
#
# @sync_to_async
# def get_product_by_id(product_id):
#     return Product.objects.get(id=product_id)
#
# @sync_to_async
# def get_colors(product):
#     return list(product.colors.all())
#
# async def show_product_colors(callback: CallbackQuery, product_id: int):
#     from bot.keyboards.get_categories_and_products import get_user_lang
#     product = await get_product_by_id(product_id)
#     lang = await get_user_lang(callback.from_user.id)
#
#     if not product:
#         await callback.message.answer("Mahsulot topilmadi.")
#         return
#
#     text = f"{hbold(product.product_name_uz if lang == 'uz' else product.product_name_ru)}:\n"
#
#     colors = await get_colors(product)  # <-- sync_to_async orqali async chaqiriq
#
#     for color in colors:
#         color_name = color.product_color_uz if lang == 'uz' else color.product_color_ru
#         price = f"{color.price} {color.currency}"
#
#         # Rasm olishni ham async qilish kerak:
#         images = await sync_to_async(list)(color.images.all())
#         if images:
#             image = images[0]
#             await callback.message.answer_photo(
#                 photo=image.image.url,
#                 caption=f"{hbold(color_name)}\nNarxi: {price}"
#             )
#         else:
#             await callback.message.answer(f"{hbold(color_name)}\nNarxi: {price}")
#
#
# @sync_to_async
# def get_color_by_id(color_id):
#     return ProductColor.objects.select_related("product").get(id=color_id)
#
# @router.callback_query(F.data.startswith("color_"))
# async def show_product_detail_by_color(callback: CallbackQuery, state: FSMContext):
#     await callback.answer()
#     color_id = int(callback.data.split("_")[1])
#     color = await get_color_by_id(color_id)
#     product = color.product
#
#     lang = await get_user_lang(callback.from_user.id)
#     name = getattr(product, f"product_name_{lang}")
#     description = getattr(product, f"product_descriptions_{lang}")
#     caption = f"<b>{name}</b>\n\n{description}"
#
#     images = await sync_to_async(list)(color.images.all())
#
#     if images:
#         for img in images:
#             if img.image:
#                 file_path = img.image.path  # local path
#                 try:
#                     photo = FSInputFile(file_path)
#                     await callback.message.answer_photo(photo=photo)
#                 except Exception as e:
#                     print("❌ Telegramga yuborilmadi:", e)
#     else:
#         await callback.message.answer("Rasmlar mavjud emas." if lang == "uz" else "Изображения отсутствуют.")
#
#     await callback.message.answer(text=caption, parse_mode="HTML")

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from app_store.models import Product, ProductColor
from django.conf import settings
from aiogram.utils.markdown import hbold



from bot.handlers.cart import get_add_to_cart_button
from bot.keyboards.utils import get_user_lang

router = Router()

# Async qilib product olish
@sync_to_async
def get_product_by_id(product_id):
    return Product.objects.get(id=product_id)

# Async qilib product ranglarini olish
@sync_to_async
def get_colors(product):
    return list(product.colors.all())

# Async qilib rang bo'yicha ProductColor olish
@sync_to_async
def get_color_by_id(color_id):
    return ProductColor.objects.select_related("product").get(id=color_id)

# Async qilib rangga tegishli rasm yo'lini olish (lokal fayl yo'li)
@sync_to_async
def get_color_images_paths(color):
    return [img.image.path for img in color.images.all() if img.image]

# Ranglar ro'yxatini ko'rsatish (rangi nomi va narxi, birinchi rasm bilan)
async def show_product_colors(callback: CallbackQuery, product_id: int):
    product = await get_product_by_id(product_id)
    if not product:
        await callback.message.answer("Mahsulot topilmadi.")
        return

    # Tilni aniqlash (sizning botda til olish funksiyangiz)
    lang = await get_user_lang(callback.from_user.id)

    text = f"{hbold(product.product_name_uz if lang == 'uz' else product.product_name_ru)}:\n\n"

    colors = await get_colors(product)

    # Har bir rang uchun rasm va narx yuborish
    for color in colors:
        color_name = color.product_color_uz if lang == 'uz' else color.product_color_ru
        price = f"{color.price} {color.currency}"

        # Rangga tegishli rasmlarni olish (lokal fayl yo'li)
        image_paths = await get_color_images_paths(color)

        caption = f"{hbold(color_name)}\nNarxi: {price}"

        if image_paths:
            # Birinchi rasmni yuboramiz
            photo = FSInputFile(image_paths[0])
            await callback.message.answer_photo(photo=photo, caption=caption)
        else:
            await callback.message.answer(caption)


# Rang bo'yicha batafsil ma'lumot va barcha rasmlar ko'rsatish
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

    image_paths = await get_color_images_paths(color)

    # Savatchaga qo‘shish tugmasi
    keyboard = get_add_to_cart_button(color.id)

    if image_paths:
        for index, img_path in enumerate(image_paths):
            photo = FSInputFile(img_path)
            if index == 0:
                # Faqat birinchi rasmda tugma bo‘ladi
                await callback.message.answer_photo(
                    photo=photo,
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=keyboard
                )
            else:
                await callback.message.answer_photo(photo=photo)
    else:
        no_img_text = "Rasmlar mavjud emas." if lang == "uz" else "Изображения отсутствуют."
        await callback.message.answer(no_img_text)
        await callback.message.answer(
            text=caption,
            parse_mode="HTML",
            reply_markup=keyboard
        )



