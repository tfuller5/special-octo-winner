import pygame
import api
import logs
from math import sqrt
from typing import Tuple
from random import randint

#print(round(testgather.gather()["main"]["temp"]-273.15, 1))
GATHERER = api.WeatherGather()
LOGGER = logs.get_logger("weather")

def distance(p1: Tuple[int], p2: Tuple[int]):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

class RainDrop():
    def __init__(self, x, y, windspeed):
        self.x = x
        self.y = y
        self.xv = randint(-50, 50)/100 + windspeed * (randint(75, 125)/100)
        self.yv = 3*(2+randint(-50, 50)/100)

    def move(self):
        self.y += self.yv
        self.x += self.xv

    def pg_rect(self):
        start = (self.x, self.y)
        end = (self.x+self.xv*2, self.y+self.yv*2)
        return start, end, distance(start, end)

    def inside_screen(self):
        size = Weather.WINDOW_SIZE
        if (self.x > size[0] or self.x < 0) and \
                (self.y > size[1] or self.y < 0):
            return False
        else:
            return True

class Cloud():
    def __init__(self, x, y, windspeed):
        self.x = x
        self.y = y
        self.xv = randint(-100, 100) / 1200 + windspeed * (randint(150, 200) / 500)
        self.yv = randint(-100, 100) / 1000
        self.size = randint(120, 160)
        f = pygame.font.SysFont("Arial", self.size)
        text = "cloud"
        # only do the thing below once!
        self.text_surface = f.render(text, True, (255, 0, 0))
        img = pygame.image.load("cloud.png")
        self.img = pygame.transform.scale(img, (self.size, self.size//3*2))


    def move(self):
        self.y += self.yv
        self.x += self.xv

    def inside_screen(self):
        size = Weather.WINDOW_SIZE
        if (self.x > size[0] or self.x < 0):
            return False
        else:
            return True

class Process:
    @staticmethod
    def _get_data(lat, lon):
        data = GATHERER.gather(lat, lon)
        return data

    @staticmethod
    def get_all_weather(lat, lon):
        data = Process._get_data(lat, lon)
        temp = round(data["main"]["temp"]-273.15)
        wtype = data["weather"][0]["main"]
        windspeed = data["wind"]["speed"] * 0.51 # wind in m/s
        return {"temp": temp, "wtype": wtype, "windspeed": windspeed}

class Weather:
    WINDOW_SIZE = (800, 600)
    CAPTION = "Weather App"
    FONT = ("Helvetica", 16)

    def __init__(self):
        self.weatherdata = None
        self.SCREEN_COLOR = (152, 245, 255)

    def start(self):
        pygame.init()
        LOGGER.info("weather-init")
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(Weather.WINDOW_SIZE)
        pygame.display.set_caption(Weather.CAPTION)

        s = self.screen.get_size()
        self.background = pygame.Surface((s[0], s[1]))
        self.background = self.background.convert()

        self.mainloop()

    @staticmethod
    def set_font(new_font: Tuple[str, int]):
        Weather.FONT = new_font

    def draw_everything(self):
        self.background.fill(self.SCREEN_COLOR)

        self.screen.fill((0, 255, 0))
        self.screen.blit(self.background, (0, 0))
        for r in self.r:
            start, end, dist = r.pg_rect()
            pygame.draw.line(self.screen, (0, 0, 255), start, end, round(20/dist))
            #pygame.draw.rect(self.screen, (0, 0, 255), r.pg_rect())
        for c in self.c:
            self.screen.blit(c.img, (c.x, c.y))

        pygame.display.flip()


    def rain_tick(self, windspeed):
        self.r.append(
            RainDrop(randint(-200, 800), randint(-100, 100), windspeed)
        )
        for r in self.r:
            r.move()
            if not r.inside_screen():
                self.r.remove(r)

    def cloud_tick(self, windspeed):
        if pygame.time.get_ticks() % 40 == 0:
            if len(self.c) <= 6:
                while True:
                    flag = False
                    x = randint(0, 400)
                    y = randint(0, 75)
                    for c in self.c:
                        if abs(c.x-x) < 50 and abs(c.y-y) < 10:
                            flag = True
                    if not flag:
                        break
                self.c.append(
                    Cloud(x, y, windspeed)
                )
                LOGGER.info("new cloud")
            else:
                LOGGER.info("too many clouds")
        for c in self.c:
            c.move()
            if not c.inside_screen():
                self.c.remove(c)


    def mainloop(self):
        LOGGER.info("start weather-mainloop")

        self.r = []
        self.c = []
        info = Process.get_all_weather(lat=51.13, lon=0.26)
        while True:

            x_wind = info["windspeed"]

            """
            if info["wtype"] == "Rain":
                self.rain_tick(x_wind)
            elif info["wtype"] == "Cloudy":
                self.cloud_tick(x_wind)
            """

            self.rain_tick(x_wind)
            self.cloud_tick(x_wind)

            if pygame.time.get_ticks() % 800 == 0:
                LOGGER.info("weather-refresh")
                info = Process.get_all_weather(lat=51.13, lon=0.26)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.draw_everything()
            self.clock.tick(40)
            

if __name__ == "__main__":
    Weather().start()