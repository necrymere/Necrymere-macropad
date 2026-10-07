import board
import busio
import displayio
import adafruit_displayio_ssd1306
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanner import MatrixScanner, DIODE_COL2ROW
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.rgb import RGB, AnimationModes

displayio.release_displays()
i2c = busio.I2C(board.D10, board.D9)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

WIDTH = 128
HEIGHT = 32
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

splash = displayio.Group()
display.show(splash)

keyboard = KMKKeyboard()

encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

encoder_handler.pins = (
    (board.D6, board.D7, None),
)

rgb_ext = RGB(
    pixel_pin=board.D8,
    num_pixels=9,
    val_limit=100,
    val_default=45,
    animation_mode=AnimationModes.STATIC,
    hue_default=120,
    sat_default=160,
)
keyboard.extensions.append(rgb_ext)

current_mode = 0
selecting_mode = False

MODES = [
    {"name": "Essentials", "file": "mode0.bmp"},
    {"name": "Editing & Navigation", "file": "mode1.bmp"},
    {"name": "Productivity", "file": "mode2.bmp"},
    {"name": "Settings", "file": "mode3.bmp"},
]

def update_screen():
    while len(splash) > 0:
        splash.pop()
    try:
        with open(MODES[current_mode]["file"], "rb") as f:
            bitmap = displayio.OnDiskBitmap(f)
            color_converter = displayio.ColorConverter(color_space=displayio.Colorspace.MONO_MSB)
            tile_grid = displayio.TileGrid(bitmap, pixel_shader=color_converter)
            splash.append(tile_grid)
    except Exception:
        pass

def flash_leds():
    rgb_ext.set_hsv(0, 0, 255) # Brief white flash on mode selection

def restore_mint_leds():
    rgb_ext.set_hsv(120, 160, rgb_ext.val_default) # Restores mint green

def encoder_callback(dir):
    global current_mode, selecting_mode
    if selecting_mode:
        current_mode = (current_mode + dir) % len(MODES)
        print(f"Mode Preview: {MODES[current_mode]['name']}")
        update_screen()
        flash_leds()
    else:
        if current_mode == 0:
            keyboard.tap_key(KC.VOLU if dir > 0 else KC.VOLD)
        elif current_mode == 1:
            keyboard.tap_key(KC.PGUP if dir > 0 else KC.PGDN)
        elif current_mode == 2:
            keyboard.tap_key(KC.LCTL(KC.TAB) if dir > 0 else KC.LCTL(KC.LSFT(KC.TAB)))
        elif current_mode == 3:
            keyboard.tap_key(KC.RGB_VAI if dir > 0 else KC.RGB_VAD)

def button_callback(state):
    global selecting_mode
    selecting_mode = not selecting_mode
    if not selecting_mode:
        keyboard.active_layers[0] = current_mode
        print(f"Locked Mode: {MODES[current_mode]['name']}")
        restore_mint_leds()
    else:
        flash_leds()
        update_screen()

encoder_handler.map = (
    ((encoder_callback, encoder_callback, button_callback),),
)


keyboard.matrix = MatrixScanner(
    row_pins=(board.D0, board.D1, board.D2),
    column_pins=(board.D3, board.D4, board.D5),
    diode_orientation=DIODE_COL2ROW,
)

# 5. KEYMAP LAYERS
keyboard.keymap = [
    # Layer 0: Essentials
    [
        KC.MUTE, KC.MPLY, KC.MNXT,
        KC.LCTL(KC.C), KC.LCTL(KC.V), KC.LCTL(KC.Z),
        KC.RGB_TOG, KC.LCTL(KC.S), KC.LCTL(KC.F),
    ],
    # Layer 1: Editing
    [
        KC.UP, KC.DOWN, KC.BSPC,
        KC.LEFT, KC.RIGHT, KC.DEL,
        KC.RGB_TOG, KC.END, KC.ENT,
    ],
    # Layer 2: Productivity
    [
        KC.LCTL(KC.T), KC.LCTL(KC.W), KC.LCTL(KC.R),
        KC.LCTL(KC.PLUS), KC.LCTL(KC.MINUS), KC.LCTL(KC.NO),
        KC.RGB_TOG, KC.TAB, KC.ESC,
    ],
    # Layer 3: Settings
    [
        KC.RGB_HUI, KC.RGB_HUD, KC.RGB_TOG,
        KC.RGB_VAI, KC.RGB_VAD, KC.NO,
        KC.RGB_MODE_RAIN, KC.RGB_MODE_PLAIN, KC.NO,
    ],
]

if __name__ == '__main__':
    update_screen()
    keyboard.go()
