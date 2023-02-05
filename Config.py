import random
import tkinter as tk
from tkinter import font
import logs


class ConfigMenu:
    SEARCH_MSG = "Type something in the entry to search for fonts"

    def __init__(self, Main):
        self.logger = logs.get_logger("configmenu")
        self.main_set_font = Main.set_font

    def start(self, window):
        # 1. use an attribute of the class:
        # 2. pass a parameter to a method:
        # use 1. when something is used everywhere
        self.logger.info("start config-menu")

        self.window = tk.Canvas(window, width=750, height=300, bg="green")
        self.window.pack()
        self.available_fonts = tk.StringVar()
        self.font_search_var = tk.StringVar()
        self.static_font = ("Helvetica", 16)
        self.set_font = ("Helvetica", 16)
        self._all_fonts = None
        self.intialise_window()

    @property
    def all_fonts(self):
        if self._all_fonts is None:
            # created ONCE, only when needed
            self._all_fonts = [name.lower() for name in font.families()]
        return self._all_fonts

    def list_available_fonts(self, *_):
        if not self.font_search_var.get():
            self.available_fonts.set("Type in a font name")
            return

        fonts_displayed = ""
        self.available_fonts.set("")
        for fontname in self.all_fonts:
            if self.font_search_var.get() in fontname:
                fonts_displayed += "\n" + fontname

        if not fonts_displayed:
            fonts_displayed = "No fonts found"

        fonts_displayed = fonts_displayed.strip()
        self.available_fonts.set(fonts_displayed)

        return 0

    def confirm_font(self, the_fox_jumped: tk.Label):
        font = self.available_fonts.get().split("\n")[0]
        font_size = int(self.option_var.get())
        output = (font, font_size)
        self.main_set_font(output)
        the_fox_jumped.config(font=(font, font_size))

    def randomize_font(self):
        fonts = (
            self.available_fonts.get().split("\n")
            if self.font_search_var.get()
            else self.all_fonts
        )
        self.font_search_var.set(random.choice(fonts))

    def randomize_font_all(self, the_fox_jumped: tk.Label):
        self.font_search_var.set(random.choice(self.all_fonts))
        self.confirm_font(the_fox_jumped)

    def intialise_window(self):
        self.option_var = tk.StringVar()
        self.option_var.set("12")

        # fmt: off
        tk.OptionMenu(
            self.window, self.option_var,
            "8", "10", "11", "12", "14", "16", "18", "20"
        ).place(x=300, y=75)
        # fmt: on
        self.available_fonts.set(ConfigMenu.SEARCH_MSG)
        la1 = tk.Label(
            self.window,
            textvariable=self.available_fonts,
            font=self.static_font,
        )

        self.font_search_var.trace_add("write", self.list_available_fonts)
        font_entry = tk.Entry(
            self.window,
            textvariable=self.font_search_var,
            width=40
        )

        the_fox_jumped = tk.Label(
            self.window, text="The brown fox jumped over the lazy dog"
        )

        confirm_button = tk.Button(
            self.window,
            text="Confirm",
            font=self.static_font,
            height=1,
            width=10,
            command=lambda *_: self.confirm_font(the_fox_jumped),
        )

        randomize_button = tk.Button(
            self.window,
            text="Random",
            font=self.static_font,
            height=1,
            width=10,
            command=lambda *_: self.randomize_font(),
        )

        def randomize(*_):
            self.randomize_font_all(the_fox_jumped)

        randomize_all_button = tk.Button(
            self.window,
            text="Random All",
            font=self.static_font,
            height=1,
            width=10,
            command=randomize,
        )

        weather_lat_entry = tk.Entry(
            self.window
        )

        weather_lon_entry = tk.Entry(
            self.window
        )

        # place everything
        the_fox_jumped.place(x=20, y=20)
        la1.place(x=20, y=130)
        font_entry.place(x=20, y=80)
        confirm_button.place(x=380, y=80)
        randomize_button.place(x=520, y=80)
        randomize_all_button.place(x=660, y=80)
        weather_lat_entry.place(x=20, y=120)
        weather_on_entry.place(x=100, y=120)
