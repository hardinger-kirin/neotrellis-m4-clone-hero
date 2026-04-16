import adafruit_trellism4
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

trellis = adafruit_trellism4.TrellisM4Express()
keyboard = Keyboard(usb_hid.devices)

COLOR_GREEN = (0, 100, 0)
COLOR_RED = (100, 0, 0)
COLOR_YELLOW = (100, 100, 0)
COLOR_BLUE = (0, 0, 100)
COLOR_ORANGE = (100, 50, 0)
COLOR_WHITE = (100, 100, 100)
COLOR_DIM_WHITE = (25, 25, 25)

COLOR_PRESSED_GREEN = (0, 25, 0)
COLOR_PRESSED_RED = (25, 0, 0)
COLOR_PRESSED_YELLOW = (25, 25, 0)
COLOR_PRESSED_BLUE = (0, 0, 25)
COLOR_PRESSED_ORANGE = (25, 12, 0)
COLOR_PRESSED_WHITE = (25, 25, 25)
COLOR_PRESSED_DIM_WHITE = (1, 1, 1)

COLOR_OFF = (0, 0, 0)

KEY_MAP = {
    (0, 0): Keycode.A,
    (1, 0): Keycode.S,
    (2, 0): Keycode.J,
    (3, 0): Keycode.K,
    (4, 0): Keycode.L,
    (7, 0): Keycode.SEMICOLON,
    (7, 3): Keycode.ENTER,
    (7, 1): Keycode.DOWN_ARROW,
    (7, 2): Keycode.UP_ARROW,
}

IDLE_COLOR_MAP = {
    (0, 0): COLOR_GREEN,
    (1, 0): COLOR_RED,
    (2, 0): COLOR_YELLOW,
    (3, 0): COLOR_BLUE,
    (4, 0): COLOR_ORANGE,
    (7, 0): COLOR_DIM_WHITE,
    (7, 3): COLOR_DIM_WHITE,
    (7, 1): COLOR_WHITE,
    (7, 2): COLOR_WHITE,
}

PRESSED_COLOR_MAP = {
    (0, 0): COLOR_PRESSED_GREEN,
    (1, 0): COLOR_PRESSED_RED,
    (2, 0): COLOR_PRESSED_YELLOW,
    (3, 0): COLOR_PRESSED_BLUE,
    (4, 0): COLOR_PRESSED_ORANGE,
    (7, 0): COLOR_PRESSED_DIM_WHITE,
    (7, 3): COLOR_PRESSED_DIM_WHITE,
    (7, 1): COLOR_PRESSED_WHITE,
    (7, 2): COLOR_PRESSED_WHITE,
}

for pos in IDLE_COLOR_MAP:
    trellis.pixels[pos] = IDLE_COLOR_MAP[pos]

pressed = set()

while True:
    current = set(trellis.pressed_keys)

    just_pressed = current - pressed
    just_released = pressed - current

    for pos in just_pressed:
        if pos in KEY_MAP:
            keyboard.press(KEY_MAP[pos])
            trellis.pixels[pos] = PRESSED_COLOR_MAP[pos]

    for pos in just_released:
        if pos in KEY_MAP:
            keyboard.release(KEY_MAP[pos])
            trellis.pixels[pos] = IDLE_COLOR_MAP[pos]

    pressed = current
