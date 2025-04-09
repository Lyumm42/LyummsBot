from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="погода"), KeyboardButton(text="курс валют")],
            [KeyboardButton(text="картинка"), KeyboardButton(text="шутка")],
            [KeyboardButton(text="список фильмов"), KeyboardButton(text="опрос")]
        ],
        resize_keyboard=True
    )


def image_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="футбол", callback_data="image_football"),
            InlineKeyboardButton(text="бокс", callback_data="image_boxing"),
            InlineKeyboardButton(text="баскетбол", callback_data="image_basketball")
        ]
    ])


def joke_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="про программистов", callback_data="joke_programming"),
            InlineKeyboardButton(text="с черным юмором", callback_data="joke_dark"),
        ]
    ])