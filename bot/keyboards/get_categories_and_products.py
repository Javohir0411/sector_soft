# from aiogram.filters import Command
# from aiogram.types import Message
# from aiogram.fsm.context import FSMContext
# from aiogram import Router, F
# from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
# from asgiref.sync import sync_to_async
# from app_store.models import Category, Product, BotUser
# from bot.keyboards.get_product_details import show_product_colors
# from config import settings
#
# router = Router()
#
#
# @sync_to_async
# def get_user_lang(telegram_id):
#     user = BotUser.objects.filter(telegram_id=telegram_id).first()
#     lang = user.lang if user else "uz"
#     if lang not in ["uz", "ru"]:
#         lang = "uz"
#     return lang
#
#
# @sync_to_async
# def get_parent_categories():
#     return list(Category.objects.filter(parent=None))
#
#
# @sync_to_async
# def get_category_by_id(category_id):
#     return Category.objects.get(id=category_id)
#
#
# @sync_to_async
# def get_subcategories(category):
#     return list(category.subcategories.all())
#
#
# @sync_to_async
# def get_products_by_category(category_id):
#     return list(Product.objects.filter(product_categories__id=category_id))
#
#
# @sync_to_async
# def get_main_image_url(product):
#     first_color = product.colors.first()
#     if first_color:
#         first_image = first_color.images.first()
#         if first_image:
#             return f"{settings.BASE_URL}{first_image.image.url}"
#     return None
#
# @router.message(Command("category"))
# async def show_categories(message: Message, state: FSMContext):
#     telegram_id = message.from_user.id
#     lang = await get_user_lang(telegram_id)
#     print(f"Lang: {lang}")
#
#     categories = await get_parent_categories()
#     keyboard = [
#         [InlineKeyboardButton(text=getattr(cat, f"category_name_{lang}"), callback_data=f"category_{cat.id}")
#          ]
#         for cat in categories
#     ]
#     text = "Kategoriyalar:" if lang == "uz" else "Категории:"
#     await message.answer(text=text, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
#                          )
#
#
# @router.callback_query(F.data.startswith("category_"))
# async def show_subcategories(callback: CallbackQuery, state: FSMContext):
#     print("✅ CALLBACK:", callback.data)
#     await callback.answer()  # Callback tugmasiga javob
#
#     category_id = int(callback.data.split("_")[1])
#     telegram_id = callback.from_user.id
#     lang = await get_user_lang(telegram_id)
#
#     category = await get_category_by_id(category_id)
#     subcategories = await get_subcategories(category)
#
#     if subcategories:  # ➕ YANGI QISM: subkategoriya bo‘lsa ularni chiqaramiz
#         keyboard = [
#             [InlineKeyboardButton(
#                 text=getattr(sub, f"category_name_{lang}"),
#                 callback_data=f"category_{sub.id}"
#             )]
#             for sub in subcategories
#         ]
#         text = "Ichki bo‘limlar:" if lang == "uz" else "Подкатегории:"
#         await callback.message.answer(
#             text=text,
#             reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
#         )
#         return
#
#     # ❗ Aks holda mahsulotlar chiqsin
#     products = await get_products_by_category(category_id)
#     if not products:
#         text = "Bu bo‘limda mahsulotlar mavjud emas." if lang == "uz" else "В этом разделе нет товаров."
#         await callback.message.answer(text)
#         return
#
#     print("Mahsulotlar soni:", len(products))
#
#     for product in products:
#         name = getattr(product, f"product_name_{lang}")
#         description = getattr(product, f"product_descriptions_{lang}")
#         caption = f"<b>{name}</b>\n\n{description}"
#
#         keyboard = InlineKeyboardMarkup(
#             inline_keyboard=[
#                 [InlineKeyboardButton(text="🛒 Batafsil", callback_data=f"product_{product.id}")]
#             ]
#         )
#
#         photo_url = await get_main_image_url(product)
#
#         if photo_url:
#             try:
#                 await callback.message.answer_photo(
#                     photo=photo_url,
#                     caption=caption,
#                     reply_markup=keyboard,
#                     parse_mode="HTML"
#                 )
#             except Exception as e:
#                 print(f"❌ Telegramga rasm yuborishda xatolik: {e}")
#                 await callback.message.answer(
#                     text=caption,
#                     reply_markup=keyboard,
#                     parse_mode="HTML"
#                 )
#         else:
#             await callback.message.answer(
#                 text=caption,
#                 reply_markup=keyboard,
#                 parse_mode="HTML"
#             )
#
# @router.callback_query(F.data.startswith("product_"))
# async def product_detail_handler(callback: CallbackQuery):
#     product_id = int(callback.data.split("_")[1])
#     await show_product_colors(callback, product_id)
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from app_store.models import Category, Product
from bot.keyboards.get_product_details import show_product_colors
from bot.keyboards.utils import get_user_lang
from config import settings

router = Router()

@sync_to_async
def get_parent_categories():
    return list(Category.objects.filter(parent=None))

@sync_to_async
def get_category_by_id(category_id):
    return Category.objects.get(id=category_id)

@sync_to_async
def get_subcategories(category):
    return list(category.subcategories.all())

@sync_to_async
def get_products_by_category(category_id):
    return list(Product.objects.filter(product_categories__id=category_id))

@sync_to_async
def get_main_image_url(product):
    first_color = product.colors.first()
    if first_color:
        first_image = first_color.images.first()
        if first_image:
            return f"{settings.BASE_URL}{first_image.image.url}"
    return None

@router.message(Command("category"))
async def show_categories(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    lang = await get_user_lang(telegram_id)

    categories = await get_parent_categories()
    keyboard = [
        [InlineKeyboardButton(text=getattr(cat, f"category_name_{lang}"), callback_data=f"category_{cat.id}")]
        for cat in categories
    ]
    text = "Kategoriyalar:" if lang == "uz" else "Категории:"
    await message.answer(text=text, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))

@router.callback_query(F.data.startswith("category_"))
async def show_subcategories(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    category_id = int(callback.data.split("_")[1])
    telegram_id = callback.from_user.id
    lang = await get_user_lang(telegram_id)

    category = await get_category_by_id(category_id)
    subcategories = await get_subcategories(category)

    if subcategories:
        keyboard = [
            [InlineKeyboardButton(text=getattr(sub, f"category_name_{lang}"), callback_data=f"category_{sub.id}")]
            for sub in subcategories
        ]
        text = "Ichki bo‘limlar:" if lang == "uz" else "Подкатегории:"
        await callback.message.answer(text=text, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
        return

    products = await get_products_by_category(category_id)
    if not products:
        text = "Bu bo‘limda mahsulotlar mavjud emas." if lang == "uz" else "В этом разделе нет товаров."
        await callback.message.answer(text)
        return

    for product in products:
        name = getattr(product, f"product_name_{lang}")
        description = getattr(product, f"product_descriptions_{lang}")
        caption = f"<b>{name}</b>\n\n{description}"

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🛒 Batafsil", callback_data=f"product_{product.id}")]
            ]
        )

        photo_url = await get_main_image_url(product)

        if photo_url:
            try:
                await callback.message.answer_photo(
                    photo=photo_url,
                    caption=caption,
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
            except Exception as e:
                print(f"❌ Telegramga rasm yuborishda xatolik: {e}")
                await callback.message.answer(
                    text=caption,
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
        else:
            await callback.message.answer(
                text=caption,
                reply_markup=keyboard,
                parse_mode="HTML"
            )

@router.callback_query(F.data.startswith("product_"))
async def product_detail_handler(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    await show_product_colors(callback, product_id)

