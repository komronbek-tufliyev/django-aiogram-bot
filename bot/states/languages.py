from aiogram.dispatcher.filters.state import State, StatesGroup

class Language(StatesGroup):
    language = State()

class ProductCount(StatesGroup):
    count = State()

    def __init__(self, ):
        self.count = 0