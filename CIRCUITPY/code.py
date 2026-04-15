import adafruit_trellism4
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

trellis = adafruit_trellism4.TrellisM4Express()
keyboard = Keyboard(usb_hid.devices)

COLOR_GREEN = (0, 100, 0)
COLOR_RED = (100, 0, 0)
COLOR_YELLOW = (50, 50, 0)
COLOR_BLUE = (0, 0, 100)
COLOR_ORANGE = (75, 25, 0)
COLOR_IDLE = (20, 20, 20)
COLOR_OFF = (0, 0, 0)

KEY_MAP = {
    (0, 0): Keycode.A,
    (1, 0): Keycode.S,
    (2, 0): Keycode.J,
    (3, 0): Keycode.K,
    (4, 0): Keycode.L,
}

COLOR_MAP = {
    (0, 0): COLOR_GREEN,
    (1, 0): COLOR_RED,
    (2, 0): COLOR_YELLOW,
    (3, 0): COLOR_BLUE,
    (4, 0): COLOR_ORANGE,
}

for pos in COLOR_MAP:
    trellis.pixels[pos] = COLOR_MAP[pos]

pressed = set()

while True:
    current = set(trellis.pressed_keys)

    just_pressed = current - pressed
    just_released = pressed - current

    for pos in just_pressed:
        if pos in KEY_MAP:
            keyboard.press(KEY_MAP[pos])
            trellis.pixels[pos] = COLOR_IDLE

    for pos in just_released:
        if pos in KEY_MAP:
            keyboard.release(KEY_MAP[pos])
            trellis.pixels[pos] = COLOR_MAP[pos]

    pressed = current
