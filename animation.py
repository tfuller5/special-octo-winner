import random
import pygame
from typing import Tuple

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


def start(size: Tuple[int, int] = (WINDOW_WIDTH, WINDOW_HEIGHT),
          caption: str = "Weather"):
    global screen, clock
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(caption)


def set_background(color: Tuple[int, int, int] = (250, 250, 250)):
    global background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(color)


def check_bounds(x, y, width, height):
    bouncex, bouncey = False, False
    if x > WINDOW_WIDTH - width:
        x = WINDOW_WIDTH - width
        bouncex = True
    if x < 0:
        x = 0
        bouncex = True
    if y > WINDOW_HEIGHT - height:
        y = WINDOW_HEIGHT - height
        bouncey = True
    if y < 0:
        y = 0
        bouncey = True
    return x, y, bouncex, bouncey


class Rectangle:
    def __init__(self):
        self.x = random.randint(1, 500)
        self.y = random.randint(1, 500)
        self.width = random.randint(10, 50)
        self.height = random.randint(10, 50)
        self.hdirection = random.randint(-5, 5)
        self.vdirection = random.randint(-5, 5)

    def move(self):
        self.x += self.hdirection
        self.y += self.vdirection
        self.x, self.y, bouncex, bouncey = check_bounds(
            self.x, self.y, self.width, self.height
        )
        if bouncex:
            self.hdirection = -self.hdirection
        if bouncey:
            self.vdirection = -self.vdirection
        self.get_collision()

    def get_collision(self):  # O(n)
        for rect1 in rectangles:
            if rect1 == self:
                continue
            ######################
            if rect1.get_pygame_rect().colliderect(self.get_pygame_rect()):
                print("smack")

    def get_pygame_rect(self):
        return pygame.rect.Rect(self.x, self.y, self.width, self.height)


def mainloop():
    global rectangles
    # rect: rectangle, x, y, w, h
    # method: colliderect

    # textpos = text.get_rect()
    # textpos

    rectangles = [Rectangle() for _ in range(10)]
    rectangles = []

    x = 1

    while True:
        clock.tick(30)
        x += 1
        background.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for r in rectangles:  # O(n)
            r.move()
            pygame.draw.rect(background, (255, 0, 0), r.get_pygame_rect())

        font = pygame.font.SysFont("Arial", 50)
        font2 = pygame.font.SysFont("Arial", 25)
        text_surface = font.render("Hello World", True, (0, 0, 255))
        text_surface2 = font2.render("Bye World", True, (255, 0, 0))
        text_surface.blit(text_surface2, (10, 20))
        background.blit(text_surface, (100 + x, 100 + x))  # surface
        # Final blit
        screen.blit(background, (0, 0))

        # print(type(screen))
        # print(type(background))
        # print(type(text_surface))
        # print(type(text_surface2))

        pygame.display.flip()


start()
set_background()
mainloop()
