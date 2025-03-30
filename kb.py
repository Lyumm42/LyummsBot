from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from main import bot


@bot.message.heandler(command=['start'])
def start_menu():
keyboard=[
    [KeyboardButton(text="Картинка"), KeyboardButton(text="Погода")],
    [KeyboardButton(text="Курс валют"), KeyboardButton(text="Список фильмов")],
    [KeyboardButton(text="Шутка"), KeyboardButton(text="Опрос")]
],



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
            InlineKeyboardButton(text="программисты", callback_data="joke_programming"),
            InlineKeyboardButton(text="черный юмор", callback_data="joke_dark"),
        ]
    ])