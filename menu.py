from aiogram import Router, types
from kb import joke_menu, image_menu, main_keyboard
from parsers import fetch_currency, fetch_weather, fetch_movies

router = Router()


@router.message()
async def menu_handler(message: types.Message):
    text = message.text.lower().strip()

    if text == "шутка":
        await message.answer("Выберите категорию шуток:", reply_markup=joke_menu())
    elif text == "/start":
        await message.answer("Привет пользователь! Вот что я могу:", reply_markup= main_keyboard())
    elif text == "погода":
        weather = await fetch_weather()
        await message.answer(weather)
    elif text == "курс валют":
        currency_data = await fetch_currency()
        if currency_data.strip():
            await message.answer(currency_data)
    elif text == "список фильмов":
        movies = await fetch_movies()
        await message.answer(movies)
    elif text == "опрос":
        await message.answer("Начнем опрос. Как вас зовут?")
    elif text == "картинка":
        await message.answer("Выберите категорию изображения:", reply_markup=image_menu())
    else:
        await message.answer("Ошибка. Неизвестная команда.")