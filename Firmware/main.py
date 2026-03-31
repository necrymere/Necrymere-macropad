# =============================================================
#  Hackpad firmware — by Necry
#  Board: XIAO RP2040 (wired) — wireless-ready for nRF52840
#
#  TO UPGRADE TO WIRELESS (nRF52840) later:
#    1. Replace "import board" pins if different
#    2. Add bluetooth module import:
#       from kb import KMKKeyboard  (nRF52840 BLE version)
#    3. Everything else (OLED, keys, RGB) stays the same!
# =============================================================

import board
import displayio
import terminalio
import busio
import time
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC, make_key
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB
from adafruit_display_text import label
from adafruit_displayio_ssd1306 import SSD1306

# ---------------------------------------------------------------
# OLED SETUP
# ---------------------------------------------------------------
displayio.release_displays()

# NOTE FOR WIRELESS UPGRADE:
#   nRF52840 uses the same I2C pins — no changes needed here!
i2c = busio.I2C(board.GPIO7, board.GPIO6)  # SCL=GPIO7, SDA=GPIO6
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = SSD1306(display_bus, width=128, height=32)

def show_screen(line1, line2):
    """Show two lines of text on the OLED"""
    group = displayio.Group()
    group.append(label.Label(
        terminalio.FONT, text=line1,
        color=0xFFFFFF, x=0, y=4
    ))
    group.append(label.Label(
        terminalio.FONT, text=line2,
        color=0xFFFFFF, x=0, y=20
    ))
    display.show(group)

def flash_screen(line1, line2, duration=1.0):
    """Show a message briefly, then return to current layer screen"""
    show_screen(line1, line2)
    time.sleep(duration)
    update_layer_screen()

def update_layer_screen():
    """Update OLED to show current layer mood"""
    layer = keyboard.active_layers[0]
    if layer == 0:
        show_screen("   Necry<3   ", "  [>_<] play! ")
    elif layer == 1:
        show_screen("   Media     ", " d(^_^)b vibe ")

# ---------------------------------------------------------------
# STARTUP SCREEN — scrolling name effect
# ---------------------------------------------------------------
show_screen("   Hackpad!  ", " (^_^)  hi!  ")
time.sleep(1.5)
show_screen("   made by   ", "   Necry<3   ")
time.sleep(1.5)

# ---------------------------------------------------------------
# KEYBOARD SETUP
# ---------------------------------------------------------------
keyboard = KMKKeyboard()

# NOTE FOR WIRELESS UPGRADE:
#   These pins are the same on nRF52840 — no changes needed!
keyboard.col_pins = (board.GPIO3, board.GPIO4, board.GPIO26)
keyboard.row_pins = (board.GPIO0, board.GPIO2, board.GPIO1)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# ---------------------------------------------------------------
# MODULES
# ---------------------------------------------------------------
layers = Layers()
keyboard.modules.append(layers)

encoder_handler = EncoderHandler()
encoder_handler.pins = ((board.GPIO27, board.GPIO28, None, False),)
keyboard.modules.append(encoder_handler)

keyboard.extensions.append(MediaKeys())

# ---------------------------------------------------------------
# RGB — wireless tip: lower val_default saves battery later!
# ---------------------------------------------------------------
rgb = RGB(
    pixel_pin=board.GPIO29,
    num_pixels=9,
    hue_default=200,   # purple-blue
    sat_default=255,
    val_default=60,    # kept low — good for battery when wireless!
)
keyboard.extensions.append(rgb)

# ---------------------------------------------------------------
# CUSTOM KEYS WITH OLED REACTIONS
# ---------------------------------------------------------------

# Copy — shows happy face
def copy_pressed(key, keyboard, *args):
    show_screen("  Shortcuts  ", " (*^*) copied!")
    time.sleep(0.8)
    update_layer_screen()
    return False

COPY = make_key(
    names=('COPY',),
    on_press=copy_pressed,
    on_release=lambda *args: None
)

# Paste — shows excited face
def paste_pressed(key, keyboard, *args):
    show_screen("  Shortcuts  ", " (^▽^) pasted!")
    time.sleep(0.8)
    update_layer_screen()
    return False

PASTE = make_key(
    names=('PASTE',),
    on_press=paste_pressed,
    on_release=lambda *args: None
)

# Undo — shows nervous face
def undo_pressed(key, keyboard, *args):
    show_screen("  Shortcuts  ", " (o_o) undo! ")
    time.sleep(0.8)
    update_layer_screen()
    return False

UNDO = make_key(
    names=('UNDO',),
    on_press=undo_pressed,
    on_release=lambda *args: None
)

# Screenshot — shows surprised face
def screenshot_pressed(key, keyboard, *args):
    show_screen("  Screenshot ", " (O_O) click! ")
    time.sleep(0.8)
    update_layer_screen()
    return False

SCREENSHOT = make_key(
    names=('SCREENSHOT',),
    on_press=screenshot_pressed,
    on_release=lambda *args: None
)

# Mute — shows dead face
def mute_pressed(key, keyboard, *args):
    show_screen("   Muted!    ", "  (x_x) shhh ")
    time.sleep(0.8)
    update_layer_screen()
    return False

MUTE = make_key(
    names=('MUTE',),
    on_press=mute_pressed,
    on_release=lambda *args: None
)

# Vol Up — shows bar
_volume = 50  # rough tracker (can't read real volume, but tracks changes)

def vol_up_pressed(key, keyboard, *args):
    global _volume
    _volume = min(100, _volume + 10)
    bars = int(_volume / 10)
    bar = '[' + '#' * bars + ' ' * (10 - bars) + ']'
    show_screen("  Volume  Up ", bar[:14])
    time.sleep(0.6)
    update_layer_screen()
    return False

VOLU = make_key(
    names=('VOLU_CUSTOM',),
    on_press=vol_up_pressed,
    on_release=lambda *args: None
)

def vol_down_pressed(key, keyboard, *args):
    global _volume
    _volume = max(0, _volume - 10)
    bars = int(_volume / 10)
    bar = '[' + '#' * bars + ' ' * (10 - bars) + ']'
    show_screen(" Volume Down ", bar[:14])
    time.sleep(0.6)
    update_layer_screen()
    return False

VOLD = make_key(
    names=('VOLD_CUSTOM',),
    on_press=vol_down_pressed,
    on_release=lambda *args: None
)

# ---------------------------------------------------------------
# KEYMAP
# ---------------------------------------------------------------
#
# LAYER 0 — APPS
#  [ Explorer ] [ Spotify ] [ Opera  ]
#  [  Steam   ] [ itch.io ] [  ---   ]
#  [   ---    ] [   ---   ] [→ Media ]
#
# LAYER 1 — MEDIA & PRODUCTIVITY
#  [   Prev   ] [Play/Pause] [  Next  ]
#  [   Copy   ] [  Paste   ] [  Undo  ]
#  [   Mute   ] [Screenshot] [→ Apps  ]

keyboard.keymap = [

    # ======= LAYER 0: APPS =======
    [
        KC.LWIN(KC.N1), KC.LWIN(KC.N2), KC.LWIN(KC.N3),  # Explorer, Spotify, Opera
        KC.LWIN(KC.N4), KC.LWIN(KC.N5), KC.NO,            # Steam, itch.io, blank
        KC.NO,          KC.NO,          KC.TO(1),          # blank, blank, → Media
    ],

    # ======= LAYER 1: MEDIA & PRODUCTIVITY =======
    [
        KC.MPRV,   KC.MPLY,    KC.MNXT,     # Prev, Play/Pause, Next
        COPY,      PASTE,      UNDO,        # Copy, Paste, Undo (with OLED reactions!)
        MUTE,      SCREENSHOT, KC.TO(0),   # Mute, Screenshot, → Apps
    ],
]

# ---------------------------------------------------------------
# ENCODER — volume with OLED bar!
# ---------------------------------------------------------------
encoder_handler.map = [
    ((VOLU, VOLD),),   # Layer 0: volume
    ((VOLU, VOLD),),   # Layer 1: volume
]

# ---------------------------------------------------------------
# OLED — update when layer changes
# ---------------------------------------------------------------
original_before_hid_send = keyboard.before_hid_send
_last_layer = -1

def before_hid_send(keyboard):
    global _last_layer
    current = keyboard.active_layers[0]
    if current != _last_layer:
        _last_layer = current
        update_layer_screen()
    original_before_hid_send(keyboard)

keyboard.before_hid_send = before_hid_send

# ---------------------------------------------------------------
# GO!
# ---------------------------------------------------------------
update_layer_screen()

if __name__ == '__main__':
    keyboard.go()
