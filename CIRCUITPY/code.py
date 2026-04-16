import adafruit_trellism4
import usb_hid
import adafruit_adxl34x
import board
import busio
import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode


# --------------------------------------------------
# COLORS
# --------------------------------------------------
COLOR_GREEN = (0, 100, 0)
COLOR_RED = (100, 0, 0)
COLOR_YELLOW = (100, 100, 0)
COLOR_BLUE = (0, 0, 100)
COLOR_ORANGE = (100, 50, 0)
COLOR_WHITE = (100, 100, 100)
COLOR_DIM_WHITE = (25, 25, 25)
COLOR_PURPLE = (100, 0, 100)

COLOR_PRESSED_GREEN = (0, 25, 0)
COLOR_PRESSED_RED = (25, 0, 0)
COLOR_PRESSED_YELLOW = (25, 25, 0)
COLOR_PRESSED_BLUE = (0, 0, 25)
COLOR_PRESSED_ORANGE = (25, 12, 0)
COLOR_PRESSED_WHITE = (25, 25, 25)
COLOR_PRESSED_DIM_WHITE = (1, 1, 1)
COLOR_PRESSED_PURPLE = (25, 0, 25)

COLOR_OFF = (0, 0, 0)


# --------------------------------------------------
# MAPPING
# --------------------------------------------------
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
    (6, 0): Keycode.H
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
    (6, 0): COLOR_PURPLE,
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
    (6, 0): COLOR_PRESSED_PURPLE,
}


# --------------------------------------------------
# INIT
# --------------------------------------------------
trellis = adafruit_trellism4.TrellisM4Express()
keyboard = Keyboard(usb_hid.devices)
i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

for pos in IDLE_COLOR_MAP:
    trellis.pixels[pos] = IDLE_COLOR_MAP[pos]

TILT_TOGGLE_POS = (6, 3)  # button to enable/disable tilt detection
trellis.pixels[TILT_TOGGLE_POS] = COLOR_RED

pressed = set()

is_tilted = False
tilt_enabled = False



# --------------------------------------------------
# HELPERS
# --------------------------------------------------
TILT_THRESHOLD = -7.0   # x must rise above this to count as tilted
UNTILT_THRESHOLD = -9.0 # x must fall below this to count as untilted
UPRIGHT_Z_MAX = 4.0     # abs(z) must be below this to count as held upright

def update_tilt():
    global is_tilted
    x, y, z = accelerometer.acceleration
    held_upright = abs(z) < UPRIGHT_Z_MAX

    if not held_upright:
        if is_tilted:
            is_tilted = False
        return

    if not is_tilted and x > TILT_THRESHOLD and y < -3.0:
        is_tilted = True
    elif is_tilted and (x < UNTILT_THRESHOLD or y > -1.0):
        is_tilted = False


# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------
while True:
    current = set(trellis.pressed_keys)
    update_tilt()

    just_pressed = current - pressed
    just_released = pressed - current

    for pos in just_pressed:
        if pos == TILT_TOGGLE_POS:
            tilt_enabled = not tilt_enabled
            trellis.pixels[TILT_TOGGLE_POS] = COLOR_GREEN if tilt_enabled else COLOR_RED
            if not tilt_enabled and is_tilted:
                is_tilted = False
                keyboard.release(Keycode.H)
        elif pos in KEY_MAP:
            keyboard.press(KEY_MAP[pos])
            trellis.pixels[pos] = PRESSED_COLOR_MAP[pos]

    for pos in just_released:
        if pos in KEY_MAP:
            keyboard.release(KEY_MAP[pos])
            trellis.pixels[pos] = IDLE_COLOR_MAP[pos]

    if tilt_enabled and is_tilted:
        keyboard.press(Keycode.H)
    else:
        keyboard.release(Keycode.H)

    pressed = current
