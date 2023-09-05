from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from api import *
from aiogram.utils.callback_data import CallbackData

basket_callback = CallbackData('mykb', 'action', 'product')
callback = CallbackData('mykb', 'action', 'count', 'product')
choose_language = ReplyKeyboardMarkup(resize_keyboard=True)
choose_language.insert(KeyboardButton('🇺🇿 O\'zbekcha')).insert(KeyboardButton('🇷🇺 Русский')).insert(KeyboardButton('🇬🇧 English'))
main_uz = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_uz.insert(KeyboardButton(text="📝 Menu")).row(KeyboardButton(text="📖 Buyurtmalarim"), KeyboardButton(text="📥 Savat"), KeyboardButton(text="⚙️ Sozlamalar"), KeyboardButton(text="✍️ Sharh qoldiring"))
main_ru = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_ru.insert(KeyboardButton(text="📝 Меню")).row(KeyboardButton(text="📖 Мои заказы"), KeyboardButton(text="📥 Корзина"), KeyboardButton(text="⚙️ Настройки"), KeyboardButton(text="✍️ Оставить отзыв"))
main_en = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_en.insert(KeyboardButton(text="📝 Menu")).row(KeyboardButton(text="📖 My orders"), KeyboardButton(text="📥 Basket"), KeyboardButton(text="⚙️ Settings"), KeyboardButton(text="✍️ Leave feedback"))


def categories(language):
    button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if language == 'uz':
        button.row(KeyboardButton(text="⬅️ Orqaga"), KeyboardButton(text="📥 Savat"))
    elif language == 'ru':
        button.row(KeyboardButton(text="⬅️ Назад"), KeyboardButton(text="📥 Корзина"))
    else:
        button.row(KeyboardButton(text="⬅️ Back"), KeyboardButton(text="📥 Basket"))
    categories = get_categories(language)
    for i in categories:
        button.insert(KeyboardButton(text=i))
    
    return button

def product_or_subcategory(category, language, product=None):
    data = category_info(language, category)
    if 'subcategory' in data:
        button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        if language == 'uz':
            button.row(KeyboardButton(text="⬅️ Orqaga"), KeyboardButton(text="📥 Savat"))
        elif language == 'ru':
            button.row(KeyboardButton(text="⬅️ Назад"), KeyboardButton(text="📥 Корзина"))
        else:
            button.row(KeyboardButton(text="⬅️ Back"), KeyboardButton(text="📥 Basket"))
        for i in data['subcategory']:
            button.insert(KeyboardButton(text=i))
        return button
    else:
        button = InlineKeyboardMarkup(row_width=2)
        data = data['products']
        if len(data) > 1:
            for i in data[1:]:
                button.add(InlineKeyboardButton(text=f"{i['name']} - {i['price']}", callback_data=basket_callback.new(action='add', product=i['id'])))
        button.row(
            InlineKeyboardButton(text=f"-", callback_data=callback.new('decrease')), 
            InlineKeyboardButton(text="1", callback_data="1"), 
            InlineKeyboardButton(text=f"+", callback_data=callback.new('increase'))
        )
        if language == 'ru':
            # add to basket
            button.add(InlineKeyboardButton(text="📥 Добавить в корзину", callback_data=basket_callback.new(action='add', product=data[0]['id'])))
        elif language == 'en':
            # add to basket
            button.add(InlineKeyboardButton(text="📥 Add to basket", callback_data=basket_callback.new(action='add', product=data[0]['id'])))
        else:
            # savatga qo'shish
            button.add(InlineKeyboardButton(text="📥 Savatga qo'shish", callback_data=basket_callback.new(action='add', product=data[0]['id'])))
        return button


############# Product #############
def product(language, product, count):
    button = InlineKeyboardMarkup()
    button.row(
        InlineKeyboardButton(text=f"-", callback_data=callback.new('decrease')),
        InlineKeyboardButton(text=f"{count}", callback_data=count),
        InlineKeyboardButton(text=f"+", callback_data=callback.new('increase'))
    )
    if language == 'ru':
        button.add(InlineKeyboardButton(text="📥 Добавить в корзину", callback_data=basket_callback.new(action='add', product=product)))
    elif language == 'en':
        button.add(InlineKeyboardButton(text="📥 Add to basket", callback_data=basket_callback.new(action='add', product=product)))
    else:
        button.add(InlineKeyboardButton(text="📥 Savatga qo'shish", callback_data=basket_callback.new(action='add', product=product)))

    return button

############## Button Settings
def settings(language):
    button = ReplyKeyboardMarkup(resize_keyboard=True, )
    button.row(InlineKeyboardButton(text="🇺🇿 O'zbekcha"), InlineKeyboardButton(text="🇷🇺 Русский"), InlineKeyboardButton(text="🇬🇧 English"))
    if language == 'ru':
        # return to main menu
        button.row(InlineKeyboardButton(text="🔝 Вернуться в главное меню",))
    elif language == 'en':
        # return to main menu
        button.row(InlineKeyboardButton(text="🔝 Return to main menu",))
    else:
        button.row(InlineKeyboardButton(text="🔝 Bosh menyuga qaytish",))

    return button

############## Button Comment ##############
def cancel(language):
    button = ReplyKeyboardMarkup(resize_keyboard=True, )
    if language == 'ru':
        # cancel
        button.row(InlineKeyboardButton(text="❌ Отменить",))
    elif language == 'en':
        # cancel
        button.row(InlineKeyboardButton(text="❌ Cancel",))
    else:
        button.row(InlineKeyboardButton(text="❌ Bekor qilish",))

    return button

############## Button Basket ##############
def mybasket(language, datas):
    button = InlineKeyboardMarkup()
    if language == 'ru':
        # cancel
        button.row(
            InlineKeyboardButton(text="🗑 Очистить корзину", callback_data=basket_callback.new(action='clear', product=0)),
            InlineKeyboardButton(text="🚖 Оформить заказ", callback_data=basket_callback.new(action='order', product=0))
        )
    elif language == 'en':
        # cancel
        button.row(
            InlineKeyboardButton(text="🗑 Clear basket", callback_data=basket_callback.new(action='clear', product=0)),
            InlineKeyboardButton(text="🚖 Checkout", callback_data=basket_callback.new(action='order', product=0))
        )
    else:
        button.row(
            InlineKeyboardButton(text="🗑 Savatni tozalash", callback_data=basket_callback.new(action='clear', product=0)),
            InlineKeyboardButton(text="🚖 Buyurtma berish", callback_data=basket_callback.new(action='order', product=0))
        )

    
    for data in datas:
        button.add(InlineKeyboardButton(text=f"❌ {data['product']}", callback_data=basket_callback.new(action='delete', product=data['product'])))

    return button

############## Get Contact ##############
def getcontact(language):
    button = ReplyKeyboardMarkup(resize_keyboard=True, )
    if language == 'uz':
        button.add(KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True))
        button.row(KeyboardButton(text="❌ Bekor qilish"))
    elif language == 'ru':
        button.add(KeyboardButton(text="📞 Отправить номер телефона", request_contact=True))
        button.row(KeyboardButton(text="❌ Отменить"))
    else:
        button.add(KeyboardButton(text="📞 Send phone number", request_contact=True))
        button.row(KeyboardButton(text="❌ Cancel"))

    return button



############## Product Button ##############
def product_button(data, language):
    button = InlineKeyboardMarkup()
    product = data[0]['product']
    if len(data) > 1:
        for i in data[1:]:
            button.add(InlineKeyboardButton(text=f"{i['name']} - {i['price']}", callback_data=basket_callback.new(action='next', product=i['id'])))
    button.row(
        InlineKeyboardButton(text=f"-", callback_data=callback.new('decrease')),
        InlineKeyboardButton(text=f"{product['count']}", callback_data=product['count']),
        InlineKeyboardButton(text=f"+", callback_data=callback.new('increase'))
    )

    if language == 'ru':
        button.add(InlineKeyboardButton(text="📥 Добавить в корзину", callback_data=basket_callback.new(action='add', count=1, product=product['id'])))
    elif language == 'en':
        button.add(InlineKeyboardButton(text="📥 Add to basket", callback_data=basket_callback.new(action='add', count=1, product=product['id'])))
    else:
        button.add(InlineKeyboardButton(text="📥 Savatga qo'shish", callback_data=basket_callback.new(action='add', count=1, product=product['id'])))

    return button

############## Payment ##############
def payment(language):
    button = ReplyKeyboardMarkup(resize_keyboard=True, )
    if language == 'uz':
        button.add("💸 Naqd")
        button.add("🟦 Click")
        button.add("🟩 Payme")
        button.row(KeyboardButton(text="⬅️ Orqaga"), KeyboardButton(text="❌ Bekor qilish"))
    elif language == 'ru':
        button.add("💸 Наличные")
        button.add("🟦 Click")
        button.add("🟩 Payme")
        button.row(KeyboardButton(text="⬅️ Назад"), KeyboardButton(text="❌ Отменить"))
    else:
        button.add("💸 Cash")
        button.add("🟦 Click")
        button.add("🟩 Payme")
        button.row(KeyboardButton(text="⬅️ Back"), KeyboardButton(text="❌ Cancel"))

    return button

############## Get Address ##############
def mylocation(language):
    button = ReplyKeyboardMarkup(resize_keyboard=True, )
    if language == 'uz':
        button.add(KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True))
        button.row(KeyboardButton(text="❌ Bekor qilish"))
    elif language == 'ru':
        button.add(KeyboardButton(text="📍 Отправить местоположение", request_location=True))
        button.row(KeyboardButton(text="❌ Отменить"))
    else:
        button.add(KeyboardButton(text="📍 Send location", request_location=True))
        button.row(KeyboardButton(text="❌ Cancel"))

############## Type of Getting Product ##############
def gettype(language):
    button = ReplyKeyboardMarkup(resize_keyboard=True, )
    if language == 'uz':
        button.add(KeyboardButton(text="🏃‍♂️ Olib ketish"))
        button.add(KeyboardButton(text="🚕 Yetkazish"))
        button.row(KeyboardButton(text="❌ Bekor qilish"))
    elif language == 'ru':
        button.add(KeyboardButton(text="🏃‍♂️ Самовывоз"))
        button.add(KeyboardButton(text="🚕 Доставка"))
        button.row(KeyboardButton(text="❌ Отменить"))
    else:
        button.add(KeyboardButton(text="🏃‍♂️ Pick up"))
        button.add(KeyboardButton(text="🚕 Delivery"))
        button.row(KeyboardButton(text="❌ Cancel"))
    
    return button

