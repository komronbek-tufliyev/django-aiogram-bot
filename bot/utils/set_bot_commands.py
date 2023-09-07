from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushirish / Запустить бота / Start the bot"),
            types.BotCommand("help", "Yordam / Помощь / Help"),
            types.BotCommand("set_language", "Tilni o'zgartirish / Изменить язык / Change language")
        ]
    )
