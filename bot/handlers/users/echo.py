from aiogram import types

from loader import dp
from keyboards.default.buttons import *


# Echo bot
# @dp.message_handler(state=None)
# async def bot_echo(message: types.Message):
#     await message.answer(message.text)

@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    language = language_info(message.from_user.id)
    print(message.text)
    text = "<i>Tushunarsiz buyruq. </i>" if language == 'uz' else "<i>Неразборчивая команда. </i>" if language == 'ru' else "<i>Unintelligible command. </i>"
    if language == 'uz':
        await message.answer(text, reply_markup=main_uz)
    elif language == 'en':
        await message.answer(text, reply_markup=main_en)
    else:
        await message.answer(text, reply_markup=main_ru)


