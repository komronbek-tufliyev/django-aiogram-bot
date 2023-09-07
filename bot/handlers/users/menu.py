from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types.input_media import InputMediaPhoto

from keyboards.default.buttons import *
from loader import dp, bot
from api import *


@dp.message_handler(text=["❌ Отменить", "❌ Bekor qilish", "❌ Cancel"])
async def cancel_function(message: types.Message):
    language = language_info(telegram_id=message.from_user.id)
    if language == 'uz':
        await message.answer("✅ Bosh menyuga xush kelibsiz\n"\
                f"🍕 Mazali pitsalar! Buyurtma berishni boshlaysizmi?", reply_markup=main_uz)
    elif language == 'ru':
        await message.answer("✅ Добро пожаловать в главное меню\n"\
                f"🍕 Вкусный пиццы! Вы начинайте заказывать?", reply_markup=main_ru)
    elif language == 'en':
        await message.answer("✅ Welcome to the main menu\n"\
                f"🍕 Delicious pizza! Shall we start ordering?", reply_markup=main_en)
        
@dp.message_handler(Text(startswith=["🍕", "🍵", "🍞", "🍰", "🧃"]))
async def subcategory_products(message: types.Message, state: FSMContext):
    await message.answer("Ok")
    await state.update_data(
        {
            'level': 'subcategory',
        }
    )
    language = language_info(telegram_id=message.from_user.id)
    key = message.text[1:]
    datas = subcategory_info(language=language, subcategory=key)
    if datas == []:
        msg = "No items found" if language == 'en' else "Mahsulotlar topilmadi" if language == 'uz' else "Товары не найдены"
        await message.answer(msg)
        return
    data = datas[0]
    print(data)
    money = "so'm" if language == 'uz' else "сум" if language == 'ru' else "sum"
    price = "💰 Narxi: " if language == 'uz' else "💰 Цена: " if language == 'ru' else "💰 Price: "
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    if language == 'uz':
        button.row(KeyboardButton(text="⬅️ Orqaga"), KeyboardButton(text="🛒 Savat"))
    elif language == 'ru':
        button.row(KeyboardButton(text="⬅️ Назад"), KeyboardButton(text="🛒 Корзина"))
    elif language == 'en':
        button.row(KeyboardButton(text="⬅️ Back"), KeyboardButton(text="🛒 Basket"))
    await message.answer(f"⬇️", reply_markup=button)
    await message.answer_photo(photo=data['image'], caption=f"<b>{data['name']}</b>\n\n{price}: {data['price']} {money}", reply_markup=product_button(data=data, language=language))


########### Function for Back Button ###########
@dp.message_handler(Text(startswith="⬅️"))
async def back_button(message: types.Message, state: FSMContext):
    data = await state.get_data()
    level = data.get('level', None)
    language = language_info(telegram_id=message.from_user.id)

    if level == 'subcategory':
        if language == 'uz':
            await message.answer("⬇️ Kategoriyani tanlang", reply_markup=categories(language))
        elif language == 'ru':
            await message.answer("⬇️ Выберите категорию", reply_markup=categories(language))
        elif language == 'en':
            await message.answer("⬇️ Choose a category", reply_markup=categories(language))
        return await state.finish()
        
    if level == 'category':
        if language == 'uz':
            await message.answer("✅ Bosh menyuga xush kelibsiz\n"\
                    f"🍕 Mazali pitsalar! Buyurtma berishni boshlaysizmi?", reply_markup=main_uz)
        elif language == 'ru':
            await message.answer("✅ Добро пожаловать в главное меню\n"\
                    f"🍕 Вкусный пиццы! Вы начинайте заказывать?", reply_markup=main_ru)
        elif language == 'en':
            await message.answer("✅ Welcome to the main menu\n"\
                    f"🍕 Delicious pizza! Shall we start ordering?", reply_markup=main_en)
        return await state.finish()
    
    elif level == 'product-category':
        await state.update_data(
            {
                'level': 'category',
            }
        )
        if language == 'uz':
            await message.answer("⬇️ Kategoriyani tanlang", reply_markup=categories(language))
        elif language == 'ru':
            await message.answer("⬇️ Выберите категорию", reply_markup=categories(language))
        elif language == 'en':
            await message.answer("⬇️ Choose a category", reply_markup=categories(language))
        return await state.finish()
    
    else:
        if language == 'uz':
            await message.answer("✅ Bosh menyuga xush kelibsiz\n"\
                    f"🍕 Mazali pitsalar! Buyurtma berishni boshlaysizmi?", reply_markup=main_uz)
        elif language == 'ru':
            await message.answer("✅ Добро пожаловать в главное меню\n"\
                    f"🍕 Вкусный пиццы! Вы начинайте заказывать?", reply_markup=main_ru)
        elif language == 'en':
            await message.answer("✅ Welcome to the main menu\n"\
                    f"🍕 Delicious pizza! Shall we start ordering?", reply_markup=main_en)
        return await state.finish()
    
########### Go to Menus ###########
@dp.message_handler(text=["📝 Menyu", "📝 Меню", "📝 Menu"])
async def category(message: types.Message, state:FSMContext):
    await state.update_data(
        {
            'level': 'category',
        }
    )
    telegram_id = message.from_user.id
    language = language_info(telegram_id=telegram_id)
    if language == 'uz':
        await message.answer("⬇️ Kategoriyani tanlang", reply_markup=categories(language))
    elif language == 'ru':
        await message.answer("⬇️ Выберите категорию", reply_markup=categories(language))
    elif language == 'en':
        await message.answer("⬇️ Choose a category", reply_markup=categories(language))


########### Go to Categories' product or Subcategory ###########
@dp.message_handler(text=get_all_categories())
async def category_product(message: types.Message, state: FSMContext):
    language = language_info(telegram_id=message.from_user.id)
    category = category_info(language=language, category=message.text)
    if 'subcategory' in category:
        await message.answer("⬇️", reply_markup=product_or_subcategory(category=message.text, language=language))
        await state.update_data(
            {
                'level': 'product-category',
            }
        )
        data = category['products'][0]
        money = "so'm" if language == 'uz' else "сум" if language == 'ru' else "sum"
        price = "💰 Narxi: " if language == 'uz' else "💰 Цена: " if language == 'ru' else "💰 Price: "
        button = ReplyKeyboardMarkup(resize_keyboard=True)

        if language == 'uz':
            button.row(KeyboardButton(text="⬅️ Orqaga"), KeyboardButton(text="🛒 Savat"))
        elif language == 'ru':
            button.row(KeyboardButton(text="⬅️ Назад"), KeyboardButton(text="🛒 Корзина"))
        elif language == 'en':
            button.row(KeyboardButton(text="⬅️ Back"), KeyboardButton(text="🛒 Basket"))
        await message.answer(f"⬇️", reply_markup=button)
        await message.answer_photo(photo=data['image'], caption=f"<b>{data['name']}</b>\n\n{price}: {data['price']} {money}", reply_markup=product_or_subcategory(category=message.text, language=language, product=data['id']))

####### Show Product ########
@dp.callback_query_handler(callback.filter())
async def decrease(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    data = callback_data
    language = language_info(telegram_id=call.from_user.id)

    if data['action'] == 'next':
        money = "so'm" if language == 'uz' else "сум" if language == 'ru' else "sum"
        price = "💰 Narxi: " if language == 'uz' else "💰 Цена: " if language == 'ru' else "💰 Price: "
        product = get_product(id=data['product'], language=language)
        await call.message.edit_media(media=InputMediaPhoto(media=product['image'], caption=f"<b>{product['name']}</b>\n\n{price}: {product['price']} {money}"), reply_markup=to_product(language=language, product=int(data['product']), count=1))
    if data['action'] == 'increase':
        money = "so'm" if language == 'uz' else "сум" if language == 'ru' else "sum"
        price = "💰 Narxi: " if language == 'uz' else "💰 Цена: " if language == 'ru' else "💰 Price: "
        count = int(data['count']) + 1
        product = get_product(id=data['product'], language=language)
        if language == 'uz':
            await call.answer(f"{int(data['count']+1)} ta")
        elif language == 'ru':
            await call.answer(f"{int(data['count']+1)} шт")
        elif language == 'en':
            await call.answer(f"{int(data['count']+1)} pcs")

        await call.message.edit_media(media=InputMediaPhoto(media=product['image'], caption=f"<b>{product['name']}</b>\n\n{price}: {product['price']} {money}"), reply_markup=to_product(language=language, product=int(data['product']), count=count))
    if data['action'] == 'decrease':
        money = "so'm" if language == 'uz' else "сум" if language == 'ru' else "sum"
        price = "💰 Narxi: " if language == 'uz' else "💰 Цена: " if language == 'ru' else "💰 Price: "
        count = int(data['count']) - 1 if int(data['count']) > 1 else 1
        product = get_product(id=data['product'], language=language)
        if language == 'uz':
            await call.answer(f"{int(data['count']-1)} ta")
        elif language == 'ru':
            await call.answer(f"{int(data['count']-1)} шт")
        elif language == 'en':
            await call.answer(f"{int(data['count']-1)} pcs")
        await call.message.edit_media(media=InputMediaPhoto(media=product['image'], caption=f"<b>{product['name']}</b>\n\n{price}: {product['price']} {money}"), reply_markup=to_product(language=language, product=int(data['product']), count=count))

    if data['action'] == 'add':
        telegram_id = call.from_user.id
        quantity = int(data['count'])
        product = int(data['product'])
        await call.message.delete()
        set_order(telegram_id=telegram_id, product=product, quantity=quantity)
        await state.update_data(
            {
                'level': 'category',
            }
        )
        if language == 'uz':
            await call.message.answer("<i>Mahsulot savatingizga qo'shildi</i>", reply_markup=categories(language))
            await call.message.answer("⬇️ Kategoriyani tanlang", reply_markup=categories(language))
        elif language == 'ru':
            await call.message.answer("<i>Товар добавлен в вашу корзину</i>", reply_markup=categories(language))
            await call.message.answer("⬇️ Выберите категорию", reply_markup=categories(language))
        elif language == 'en':
            await call.message.answer("<i>The product has been added to your cart</i>", reply_markup=categories(language))
            await call.message.answer("⬇️ Choose a category", reply_markup=categories(language))
            

