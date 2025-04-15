import aiohttp
import os
import random

from bs4 import BeautifulSoup


async def get_currency():
    url = "https://valuta.kg/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                currency_names = []
                names_table = soup.find("table", class_="kurs-table")
                if names_table:
                    rows = names_table.find_all("tr")[1:]
                    for row in rows:
                        currency_div = row.find("div", class_="rate-name")
                        if currency_div:
                            currency_names.append(currency_div.text.strip())
                exchange_rates = []
                rates_table = soup.find_all("table", class_="kurs-table")[1]
                if rates_table:
                    rows = rates_table.find_all("tr")
                    for row in rows:
                        cols = row.find_all("td")
                        if len(cols) >= 2:
                            buy_price = cols[0].text.strip()
                            sell_price = cols[1].text.strip()
                            exchange_rates.append((buy_price, sell_price))
                if currency_names and exchange_rates and len(currency_names) == len(exchange_rates):
                    message = "*Курс валют в Бишкеке:*\n"
                    for i in range(len(currency_names)):
                        message += f"*{currency_names[i].upper()}*:\n   Покупка: `{exchange_rates[i][0]}` \n   Продажа: `{exchange_rates[i][1]}`\n\n"
                    return message
                else:
                    return "Ошибка. Попробуйте позже."
            return "Ошибка при подключении к сайту курса валют."


async def get_weather():
    url = 'https://wttr.in/Bishkek?format=%C|%t|%w|%h'
    headers = {"User-Agent": "Mozilla/5.0"}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    weather, temp, wind, humidity = (await response.text()).split("|")
                    return (f"Погода в Бишкеке сейчас:\n"
                            f"{weather}\n"
                            f"Температура: {temp}\n"
                            f"Влажность: {humidity}\n"
                            f"Ветер: {wind}\n")
                return "Ошибка при запросе погоды."
        except Exception:
            return "Ошибка. Не удалось получить прогноз."


async def get_movies():
    url = "https://kg.kinoafisha.info/bishkek/movies/"
    headers = {"User-Agent": "Mozilla/5.0"}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")

                    movies = [
                        movie.text.strip()
                        for movie in soup.select(".movieItem_title")
                        if movie.text.strip()
                    ]

                    return (
                        "Фильмы в прокате:\n" + "\n".join(f"{movie}" for movie in movies)
                        if movies else "Не удалось найти фильмы."
                    )
                return "Ошибка соединения."
        except Exception:
            return "Ошибка. Не удалось загрузить фильмы."


async def get_joke(category="Any"):
    url = f"https://v2.jokeapi.dev/joke/{category}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data["type"] == "single":
                    return data["joke"]
                else:
                    return f"{data['setup']}\n{data['delivery']}"
            else:
                return "Ошибка. Попробуйте позже."


async def get_random_images(category: str):
    folder_path = f"images/{category}/"
    images = [img for img in os.listdir(folder_path) if img.endswith(".jpg")]
    random_images = random.sample(images, min(1, len(images)))
    return [folder_path + img for img in random_images]