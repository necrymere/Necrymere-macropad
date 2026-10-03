import board
import busio
import displayio
import adafruit_displayio_ssd1306

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler

keyboard = KMKKeyboard()

# ==========================================
# 1. MODULES & HARDWARE SETUP
# ==========================================
layers = Layers()
encoder_handler = EncoderHandler()
keyboard.modules = [layers, encoder_handler]

# Pin Assignments (Seeed XIAO)
keyboard.pins = [board.D3, board.D6, board.D7, board.D8]

# Rotary Encoder (Phase A: D0, Phase B: D1, Push Switch: D2)
encoder_handler.pins = ((board.D0, board.D1, board.D2, False),)

# ==========================================
# 2. OLED DISPLAY ENGINE (SSD1306 - 128x32)
# ==========================================
displayio.release_displays()
i2c = busio.I2C(board.SCL, board.SDA)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

current_layer = -1

def update_display(layer_idx):
    global current_layer
    if layer_idx == current_layer:
        return
    current_layer = layer_idx
    
    bmp_filename = f"mode{layer_idx}.bmp"
    try:
        bitmap = displayio.OnDiskBitmap(bmp_filename)
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
        group = displayio.Group()
        group.append(tile_grid)
        display.root_group = group
    except Exception as e:
        print(f"Failed to load {bmp_filename}: {e}")

# Load initial Mode 0 image on boot
update_display(0)

# Layer observer to swap BMP assets automatically on layer changes
class OLEDLayerSync:
    def during_bootup(self, keyboard):
        pass
    def before_matrix_scan(self, keyboard):
        pass
    def after_matrix_scan(self, keyboard):
        pass
    def before_hid_send(self, keyboard):
        pass
    def after_hid_send(self, keyboard):
        if keyboard.active_layers:
            update_display(keyboard.active_layers[0])

keyboard.modules.append(OLEDLayerSync())

# ==========================================
# 3. ENCODER MAP (CW, CCW, Push Button)
# ==========================================
encoder_handler.map = (
    # Mode 0: Essentials (Volume Up, Volume Down, Mute)
    ((KC.AUDIO_VOL_UP, KC.AUDIO_VOL_DOWN, KC.AUDIO_MUTE),),
    
    # Mode 1: Editing (Scrub Right, Scrub Left, Undo)
    ((KC.RIGHT, KC.LEFT, KC.LCTRL(KC.Z)),),
    
    # Mode 2: Productivity (Scroll Down, Scroll Up, Next Tab)
    ((KC.PGDN, KC.PGUP, KC.LCTRL(KC.TAB)),),
    
    # Mode 3: Settings (Brightness Up, Brightness Down, Return to Mode 0)
    ((KC.BRIGHTNESS_UP, KC.BRIGHTNESS_DOWN, KC.TO(0)),),
)

# ==========================================
# 4. KEYMAP (4 Modes)
# ==========================================
keyboard.keymap = [
    # Mode 0: Essentials
    [
        KC.MPLY,      # Key 1: Play/Pause
        KC.MNXT,      # Key 2: Next Track
        KC.MPRV,      # Key 3: Previous Track
        KC.TO(1),     # Key 4: Switch to Mode 1
    ],
    
    # Mode 1: Editing & Navigation
    [
        KC.LCTRL(KC.C), # Key 1: Copy
        KC.LCTRL(KC.V), # Key 2: Paste
        KC.LCTRL(KC.Z), # Key 3: Undo
        KC.TO(2),       # Key 4: Switch to Mode 2
    ],
    
    # Mode 2: Productivity
    [
        KC.LALT(KC.TAB), # Key 1: App Switcher
        KC.LCTRL(KC.T),  # Key 2: New Tab
        KC.LCTRL(KC.W),  # Key 3: Close Tab
        KC.TO(3),        # Key 4: Switch to Mode 3
    ],
    
    # Mode 3: Settings
    [
        KC.LCTRL(KC.LALT(KC.DEL)), # Key 1: Task Manager / Lock
        KC.NO,                     # Key 2: Reserved
        KC.NO,                     # Key 3: Reserved
        KC.TO(0),                  # Key 4: Loop back to Mode 0
    ],
]

if __name__ == '__main__':
    keyboard.go()
