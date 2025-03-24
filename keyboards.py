from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="погода"), KeyboardButton(text="курс валют")],
        [KeyboardButton(text="картинка"), KeyboardButton(text="опрос")],
        [KeyboardButton(text="список фильмов"), KeyboardButton(text="шутка")]
    ],
    resize_keyboard=True
)


def joke_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="черный юмор", callback_data="joke_dark"),
        ]
    ])


def image_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="футбол", callback_data="image_football"),
            InlineKeyboardButton(text="бокс", callback_data="image_boxing"),
            InlineKeyboardButton(text="баскетбол", callback_data="image_basketball")
        ]
    ])