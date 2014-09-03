SIZE = (640, 480)
FPS = 30




class Item:
    def __init__(self, rect, text, base_price, base_cps_each):
        self.rect = rect
        self.text = text
        self.count = 0
        self.base_price = base_price
        self.cps_each = base_cps_each

    def draw(self, surface):
        #draw background
        pygame.draw.rect(surface, BUTTON_BG_COLOR, self.rect, 0)
        #draw border
        pygame.draw.rect(surface, BUTTON_BG_COLOR, self.rect, 2)
        #draw text
        text_surface = FONT.render(str(self.count) + "x" + self.text + " $" + str(int(self.price())), False, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (self.rect.left + 10, self.rect.top + self.rect.height * 0.25)
        surface.blit(text_surface, text_rect)

    def total_cps(self):
        return self.cps_each * self.count

    def price(self):
        return self.base_price * 1.15**self.count

    def click(self):
        price = self.price()
        global COOKIES
        if COOKIES >= price:
            self.count += 1
            COOKIES -= price

    def collidepoint(self, point):
        return self.rect.collidepoint(point)


import sys
import pygame
from pygame.locals import *

pygame.init()

fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("cookieclicker")

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

BUTTON_BG_COLOR = pygame.Color(68, 93, 255)
BUTTON_BORDER_COLOR = pygame.Color(85, 50, 232)

FONT = pygame.font.SysFont("sysfont", 24)

COOKIE_IMAGE = pygame.image.load("cookie.png")

COOKIES = 0
CPS = 0.0


def make_items(text_list, base_price_list, cps_list, rect, spacing):
    button_height = rect.height / len(text_list)
    button_width = rect.width
    buttons = []
    for i in range(len(text_list)):
        text = text_list[i]
        base_price = base_price_list[i]
        base_cps = cps_list[i]
        button_rect = Rect(rect.left, rect.top + i * (button_height + spacing), button_width, button_height)
        button = Item(button_rect, text, base_price, base_cps)
        buttons.append(button)
    return buttons


cookie_rect = Rect(25, 250, COOKIE_IMAGE.get_width(), COOKIE_IMAGE.get_height())


def click_cookie():
    global COOKIES
    COOKIES += 1


items = make_items(["Cursor", "Grandma", "Farm", "Factory", "Mine", "Shipment", "Alchemy Lab", "Portal",
                    "Time machine", "Antimatter condenser", "Prism"],
                   [15, 100, 500, 3000, 10000, 40000, 200000, 1666666, 123456789, 3999999999, 75000000000],
                   [0.1, 0.5, 4, 10, 40, 100, 400, 6666, 98765, 999999, 10000000],
                   Rect(400, 25, 230, 400), 5)


def calculate_cps():
    global CPS
    cps = 0.0
    for item in items:
        cps += item.total_cps()
    CPS = cps

def update_cookies():
    global COOKIES
    COOKIES += CPS / FPS

while True:
    screen.fill(BLACK)
    screen.blit(COOKIE_IMAGE, cookie_rect)

    #draw cookies count
    text_surface = FONT.render(str(int(COOKIES)) + "+" + str(CPS) + "CPS", False, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (100, 200)
    screen.blit(text_surface, text_rect)

    for button in items:
        button.draw(screen)

    calculate_cps()
    update_cookies()


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            mouse_button = event.button
            if mouse_button == 1:
                for button in items:
                    if button.collidepoint(mouse_pos):
                        button.click()
                        break
                if cookie_rect.collidepoint(mouse_pos):
                    click_cookie()

    pygame.display.update()
    fpsClock.tick(FPS)
