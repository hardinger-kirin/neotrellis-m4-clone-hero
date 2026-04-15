import adafruit_trellism4
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

trellis = adafruit_trellism4.TrellisM4Express()
keyboard = Keyboard(usb_hid.devices)

# Map (col, row) button positions to keycodes and LED colors.
# The Trellis M4 grid is 8 columns x 4 rows.
KEY_MAP = {
    (0, 0): Keycode.W,
    (1, 0): Keycode.A,
    (2, 0): Keycode.S,
    (3, 0): Keycode.D,
}

COLOR_ON = (0, 100, 0)   # green when held
COLOR_IDLE = (20, 20, 20) # dim white when idle
COLOR_OFF = (0, 0, 0)

# Light up mapped buttons so you know which ones do something
for pos in KEY_MAP:
    trellis.pixels[pos] = COLOR_IDLE

pressed = set()

while True:
    current = set(trellis.pressed_keys)

    just_pressed = current - pressed
    just_released = pressed - current

    for pos in just_pressed:
        if pos in KEY_MAP:
            keyboard.press(KEY_MAP[pos])
            trellis.pixels[pos] = COLOR_ON

    for pos in just_released:
        if pos in KEY_MAP:
            keyboard.release(KEY_MAP[pos])
            trellis.pixels[pos] = COLOR_IDLE

    pressed = current
