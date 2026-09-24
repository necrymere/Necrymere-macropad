#  MintPad

A clean, customizable 4-mode macropad driven by **KMK Firmware** and **CircuitPython 9.x**. Designed around a Seeed Studio XIAO microcontroller, **MintPad** pairs a 128x32 monochrome OLED screen with a rotary encoder for effortless layer toggling and real-time visual feedback.

---

##  Features

* **4 Dedicated Workspaces:** Instantly switch between media controls, editing shortcuts, productivity tools, and device settings.
* **Dynamic OLED Display:** 1-bit typography graphics (`mode0.bmp` – `mode3.bmp`) update instantly on layer changes.
* **Rotary Encoder Integration:** Smooth, responsive control for volume, timeline scrubbing, or page scrolling with an integrated push-button switch.
* **On-the-Fly Configuration:** Powered by CircuitPython—tweak keymaps or swap graphics directly via USB without compiling code.

---

## 🔌 Hardware & Pinout Mapping

### Recommended Components
* **Microcontroller:** Seeed Studio XIAO (RP2040, SAMD21, or ESP32-S3)
* **Display:** 0.91" I2C OLED (SSD1306 driver, 128x32 resolution)
* **Inputs:** Mechanical key switches + Rotary encoder with push button

### Default Wiring Scheme

| Component | Signal / Line | Seeed XIAO Pin |
| :--- | :--- | :--- |
| **OLED Screen** | SDA | `SDA` / `D4` |
| **OLED Screen** | SCL | `SCL` / `D5` |
| **Rotary Encoder** | Phase A | `D0` |
| **Rotary Encoder** | Phase B | `D1` |
| **Rotary Encoder** | Push Switch | `D2` |
| **Key Matrix / Switches** | Direct Inputs | `D3`, `D6`, `D7`, `D8`... |

---

##  Layer Breakdown

| Mode | Name | OLED Asset | Encoder Function | Primary Focus |
| :---: | :--- | :---: | :--- | :--- |
| **0** | **Essentials** | `mode0.bmp` | Master Volume | Media playback, track skipping, system volume |
| **1** | **Editing & Navigation** | `mode1.bmp` | Timeline Scrub | Cut, copy, paste, undo, redo, selection |
| **2** | **Productivity** | `mode2.bmp` | Page Scroll | Workspace switching, app launchers, browser tabs |
| **3** | **Settings** | `mode3.bmp` | Utility / Adjust | Display toggles, board status, hardware utilities |

---

##  Directory Layout

Organize your `CIRCUITPY` drive before booting:

```text
CIRCUITPY/
├── code.py                           # Main KMK keymap & display engine
├── mode0.bmp                         # 128x32 monochrome graphic for Mode 0
├── mode1.bmp                         # 128x32 monochrome graphic for Mode 1
├── mode2.bmp                         # 128x32 monochrome graphic for Mode 2
├── mode3.bmp                         # 128x32 monochrome graphic for Mode 3
└── lib/
    ├── kmk/                          # Complete KMK firmware library
    └── adafruit_displayio_ssd1306.mpy # SSD1306 driver module
