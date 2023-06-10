import requests
import datetime
from pprint import pprint
from config import open_weather_token


def get_weather(city, open_weather_token):

    code_to_smile = {
        "Clear": "Ochiq \U00002600",
        "Clouds": "Bulutli \U00002601",
        "Rain": "Yomg'ir \U00002614",
        "Drizzle": "Yomg'ir \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Qor \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        pprint(data)

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

        print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Ob havo: {city}\nТемпература: {cur_weather}C° {wd}\n"
              f"Namlik: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
              f"Quyosh chiqishi: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
              f"Xayrli kun!!"
              )

    except Exception as ex:
        print(ex)
        print("Shahar nomini tekshiring")


def main():
    city = input("Shahar nomini kiriting: ")
    get_weather(city, open_weather_token)


if __name__ == '__main__':
    main()
