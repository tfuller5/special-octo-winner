import json
from datetime import datetime

import requests

import logs

import pgeocode

"""
DOCUMENTATION

https://openweathermap.org/current
https://openweathermap.org/weather-conditions

clear sky
few clouds
scattered clouds
broken clouds
shower rain
rain
thunderstorm
snow
mist


Thunderstorm
Drizzle
Rain
Snow
Atmosphere
Clear
Clouds
"""

# googledoc
# - multiple files, images
# - run the files

logger = logs.get_logger("api")

def locate(postcode = "cb1"):
    nomi = pgeocode.Nominatim('gb')
    data = nomi.query_postal_code(postcode)
    print(data)



class Gatherer:
    def __init__(self, key, url):
        logger.info("start data-gather-api")
        self.key = key
        self.url = url

    def gather(self) -> dict:
        logger.info("data gathering")
        response = requests.get(self.url)
        data: dict = json.loads(response.text)
        return data


class WeatherGather(Gatherer):
    def __init__(self):
        logger.info("start weather-gather-api")
        self.key = "a90bfae811717913022120168c4a1a6f"

        super().__init__(self.key, None)

    def _gen_url(self, lat=51.13, lon=0.26): # private!
        return f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.key}"

    def gather(self, lat=51.13, lon=0.26) -> dict:
        logger.info("data gathering")
        response = requests.get(self._gen_url(lat, lon))
        data: dict = json.loads(response.text)
        return data


if __name__ == "__main__":
    #testgather = WeatherGather()
    #print(testgather.gather())
    locate()
