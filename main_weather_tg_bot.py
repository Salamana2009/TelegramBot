import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Salom! Menga shahar nomini yuboring, men sizga ob-havo hisobotini yuboraman!")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "ochiq\U00002600",
        "Clouds": "bulutli \U00002601",
        "Rain": "Yomg'ir \U00002614",
        "Drizzle": "Yomg'ir \U00002614",
        "Thunderstorm": "Chaqmoq \U000026A1",
        "Snow": "Qor \U0001F328",
        "Mist": "Tuman \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Derazadan tashqariga qarang, u erda ob-havo qandayligini tushunmayapman!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Ob havo: {city}\nHarorat: {cur_weather}C° {wd}\n"
              f"Namlik: {humidity}%\nBosim: {pressure} мм.рт.ст\nShamol: {wind} м/с\n"
              f"Quyosh chiqishi: {sunrise_timestamp}\nQuyosh botishi: {sunset_timestamp}\nKun: {length_of_the_day}\n"
              f"***Xayrli kun!***"
              )

    except:
        await message.reply("\U00002620 Shahar nomini tekshiring \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)
