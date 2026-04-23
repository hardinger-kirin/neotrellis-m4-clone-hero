# neotrellis-m4-clone-hero

A CircuitPython firmware that turns the [Adafruit NeoTrellis M4 Express](https://www.adafruit.com/product/3938) into a USB HID controller for [Clone Hero](https://clonehero.net/). The device appears to your computer as a keyboard, so no drivers or special software are needed — just plug it in and play.

## Button layout

The NeoTrellis M4 has an 8×4 grid of RGB buttons. Only the buttons below are mapped; all others are ignored.

```
Col:  0      1      2      3      4      5  6      7
     ┌──────┬──────┬──────┬──────┬──────┬──┬──────┬──────┐
Row0 │  A   │  S   │  J   │  K   │  L   │  │  H   │  ;   │
     │Green │ Red  │Yellow│ Blue │Orange│  │Purple│Whammy│
     ├──────┼──────┼──────┼──────┼──────┼──┼──────┼──────┤
Row1 │      │      │      │      │      │  │      │  ↑   │
     ├──────┼──────┼──────┼──────┼──────┼──┼──────┼──────┤
Row2 │      │      │      │      │      │  │      │  ↓   │
     ├──────┼──────┼──────┼──────┼──────┼──┼──────┼──────┤
Row3 │      │      │      │      │      │  │Tilt  │ Enter│
     │      │      │      │      │      │  │Toggle│      │
     └──────┴──────┴──────┴──────┴──────┴──┴──────┴──────┘
```

| Button | Key | Clone Hero action |
|--------|-----|-------------------|
| Col 0, Row 0 (Green) | `A` | Green fret |
| Col 1, Row 0 (Red) | `S` | Red fret |
| Col 2, Row 0 (Yellow) | `J` | Yellow fret |
| Col 3, Row 0 (Blue) | `K` | Blue fret |
| Col 4, Row 0 (Orange) | `L` | Orange fret |
| Col 6, Row 0 (Purple) | `H` | Star Power |
| Col 7, Row 0 (White) | `;` | Whammy |
| Col 7, Row 1 (White) | `↑` | Strum up |
| Col 7, Row 2 (White) | `↓` | Strum down |
| Col 7, Row 3 (White) | `Enter` | Start / Pause |
| Col 6, Row 3 | — | Tilt toggle (see below) |

Each mapped button lights up in its corresponding color at idle and dims when pressed.

> **Clone Hero keybindings:** The keys above (`A`, `S`, `J`, `K`, `L`, `H`, `;`, `↑`, `↓`, `Enter`) must be configured in Clone Hero's controller settings to match your fret, strum, whammy, star power, and pause assignments.

## Accelerometer tilt detection

The NeoTrellis M4 has an onboard accelerometer. When tilt detection is enabled, tilting the board activates Star Power by holding `H` — no button press needed.

**Tilt toggle button (Col 6, Row 3):**
- **Red** — tilt detection is off (default on startup)
- **Green** — tilt detection is on

Press this button to toggle tilt detection on or off at any time. Disabling it while the board is tilted immediately releases `H`.

The Star Power key (`H`) can also be pressed manually at any time using the Col 6, Row 0 button regardless of tilt state.

## Hardware

- [Adafruit NeoTrellis M4 Express](https://www.adafruit.com/product/3938) (with or without the optional enclosure)

## Prerequisites

1. **CircuitPython** — install the latest stable CircuitPython UF2 for the NeoTrellis M4 from the [CircuitPython downloads page](https://circuitpython.org/board/trellis_m4_express/).

2. **CircuitPython libraries** — download the [Adafruit CircuitPython Library Bundle](https://circuitpython.org/libraries) matching your CircuitPython version and copy the following into the `lib/` folder on your `CIRCUITPY` drive:
   - `adafruit_trellism4.mpy`
   - `adafruit_hid/` (entire folder)
   - `adafruit_adxl34x.mpy`

## Deployment

1. Connect the NeoTrellis M4 to your computer via USB.
2. If it isn't already running CircuitPython, double-press the reset button to enter the UF2 bootloader and drag the CircuitPython `.uf2` file onto the `TRELLIS4BOOT` drive that appears.
3. After the board reboots, a `CIRCUITPY` drive will mount on your computer.
4. Copy the contents of this repo's [`CIRCUITPY/`](CIRCUITPY/) folder onto the root of that drive, so the structure looks like:
   ```
   CIRCUITPY/
   ├── code.py
   ├── lib/
   │   ├── adafruit_trellism4.mpy
   │   ├── adafruit_hid/
   │   └── adafruit_adxl34x.mpy
   └── sd/
   ```
5. The board will automatically restart and run `code.py`. The mapped buttons will light up and the device will be ready to use as a keyboard.

## Customizing key bindings

Key-to-keycode mappings are defined in [`CIRCUITPY/code.py`](CIRCUITPY/code.py) in the `KEY_MAP` dictionary. Button coordinates are `(column, row)` with `(0, 0)` at the top-left of the grid. Valid keycodes are found in the [`adafruit_hid.keycode`](https://docs.circuitpython.org/projects/hid/en/latest/api.html#adafruit_hid.keycode.Keycode) module.

Button colors can be changed by editing the `IDLE_COLOR_MAP` and `PRESSED_COLOR_MAP` dictionaries. Colors are `(R, G, B)` tuples with values from `0` to `255`.

The tilt detection thresholds can be tuned via the `TILT_THRESHOLD`, `UNTILT_THRESHOLD`, and `UPRIGHT_Z_MAX` constants near the top of `code.py`.
