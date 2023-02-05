import logs
import tkinter as tk
from typing import Tuple, Optional

from Config import ConfigMenu
from Weather import Weather


# app in python: 50 servers all running the app
# logger = logging.Logger(name = "hi")
# logger.setLevel(logging.INFO)
# logger.info("message")
# logger.warning("this is a warning")


# Tk , widgets, master, except the window
# Label, font Helvetica
# 2. pack, grid, place methods: for design

# drop down menu, with fonts
# select a font
# Entry widget, Label, textvariable StringVar


class Main:
    example = 5
    FONT = ("Helvetica", 16)

    def __init__(self,
                 config: Optional[ConfigMenu]=None,
                 weather: Optional[Weather]=None):
        self.config = config
        self.weather = weather
        self.logger = logs.get_logger("main")

        self.config_started = False

    def set_config(self, config: ConfigMenu):
        self.config = config

    def set_weather(self, weather: Weather):
        self.weather = weather

    def start_mainloop(self):
        # 1. use an attribute of the class:
        # 2. pass a parameter to a method:
        # use 1. when something is used everywhere
        self.logger.info("starting mainloop")
        self.window = tk.Tk()
        self.window.geometry("750x450")
        self.intialise_first_window()
        self.window.mainloop()

    def switch_to_weather(self):
        self.weather.start()


    def switch_to_config(self):
        if not self.config_started:
            self.config.start(self.window)
            self.config_started = True
        else:
            self.config.window.pack()

    @staticmethod
    def set_font(new_font: Tuple[str, int]):
        Main.FONT = new_font
        Weather.set_font(new_font)

    def intialise_first_window(self):
        to_weather_button = tk.Button(
            self.window,
            text="Weather",
            font=self.FONT,
            height=1,
            width=10,
            command=lambda *_: self.switch_to_weather(),
        )
        to_config_button = tk.Button(
            self.window,
            text="Config",
            font=self.FONT,
            height=1,
            width=10,
            command=lambda *_: self.switch_to_config(),
        )

        to_weather_button.place(x=200, y=400)
        to_config_button.place(x=350, y=400)


if __name__ == "__main__":
    # main is the object
    # Main is the class
    weather = Weather()
    # decide if main should save config or
    #           config should save main
    main = Main(None, weather)
    config = ConfigMenu(main)
    main.set_config(config)
    main.start_mainloop()
