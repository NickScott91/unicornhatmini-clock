#!/usr/bin/env python3

import time
import datetime
from gpiozero import Button
from unicornhatmini import UnicornHATMini
from random import randrange
from signal import pause

unicornhatmini = UnicornHATMini()

bright = 0.05
red = 150
green = 150
blue = 50
dotson = True
previousMinute = -1
mode = 'time'

unicornhatmini.set_brightness(bright)

numbers = {
    "0": [[2, 0], [1, 0], [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 6], [2, 6], [2, 5], [2, 4], [2, 3], [2, 2], [2, 1]],
    "1": [[0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [0, 6], [2, 6]],
    "2": [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [1, 3], [0, 4], [0, 5], [0, 6], [1, 6], [2, 6]],
    "3": [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [2, 3], [1, 3], [0, 3], [2, 4], [2, 5], [2, 6], [1, 6], [0, 6]],
    "4": [[0, 0], [0, 1], [0, 2], [0, 3], [1, 3], [2, 3], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6]],
    "5": [[0, 0], [1, 0], [2, 0], [0, 1], [0, 2], [0, 3], [1, 3], [2, 3], [2, 4], [2, 5], [2, 6], [1, 6], [0, 6]],
    "6": [[2, 0], [1, 0], [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 6], [2, 6], [2, 5], [2, 4], [2, 3], [1, 3]],
    "7": [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [2, 3], [1, 4], [1, 5], [1, 6]],
    "8": [[2, 0], [1, 0], [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 6], [2, 6], [2, 5], [2, 4], [2, 3], [1, 3], [2, 2], [2, 1]],
    "9": [[2, 0], [1, 0], [0, 0], [0, 1], [0, 2], [0, 3], [0, 6], [1, 6], [2, 6], [2, 5], [2, 4], [2, 3], [1, 3], [2, 2], [2, 1]],
    ":": [[1, 2], [1, 4]],
    ".": [[1, 6]]
}

button_a = Button(5)
button_b = Button(6)
button_x = Button(16)
button_y = Button(24)

def toggle_display(button):
    global mode
    if mode == 'time':
        mode = 'date'
    elif mode == 'date':
        mode = 'time'


def change_color():
    global red
    global green
    global blue
    red = randrange(256)
    green = randrange(256)
    blue = randrange(256)


def increase_brightness():
    global bright
    if bright >= 0.9:
        pass
    else:
        bright += 0.05


def decrease_brightness():
    global bright
    if bright <= 0.1:
        pass
    else:
        bright -= 0.05


button_a.when_pressed = toggle_display
button_b.when_pressed = change_color
button_x.when_pressed = increase_brightness
button_y.when_pressed = decrease_brightness


def letter(char, offset):
    for pixel in numbers[char]:
        x = pixel[0] + offset
        y = pixel[1]
        unicornhatmini.set_pixel(x, y, red, green, blue)
        unicornhatmini.set_brightness(bright)


def show_time(now):
    global dotson
    unicornhatmini.clear()
    timestring = now.strftime("%H%M")
    letter(timestring[0], 0)
    letter(timestring[1], 4)
    if dotson == True:
        letter(":", 7)
    letter(timestring[2], 10)
    letter(timestring[3], 14)
    unicornhatmini.show()


def show_date(now):
    global dotson
    unicornhatmini.clear()
    timestring = now.strftime("%d%m")
    letter(timestring[0], 0)
    letter(timestring[1], 4)
    letter(".", 7)
    letter(timestring[2], 10)
    letter(timestring[3], 14)
    unicornhatmini.show()


while True:
    now = datetime.datetime.now()

    if mode == 'time':
        show_time(now)

    if mode == 'date':
        show_date(now)

    dotson = not dotson
    previousMinute = now.minute
    time.sleep(0.5)