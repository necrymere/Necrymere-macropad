#  MintPad

 A 9 key macropad with a rotary encoder, backlight and OLED display. It uses KMK firmware.

 I made it mostly because I am a multitasker and I think it will help me. Also made it really modular cause I do a lot of things and I love flexibility.


 ## Features:

 -Blank case with an engraving on the backside to leave space for me to decorate the rest however I feel like in the moment.
 -OLED display for showing what mode it is in/silly things that I have yet to think about
 -EC11 Rotary encoder for volume control(and once pressed for changing the modes)
 -9 LEDs, one for each key to let me customise the colour of it based on my vibe(curently my setup is mint green so I programed it that way)
 -9 keys
 - 4 modes at the moment of writing this(probably will add more and hopefully adjust this count too)

 ## CAD Model:
 Everything should fit with screws(not sure what size but I will figure it out when I get it and go to the hardware store to buy some) or I will just glue the two parts but it is not the best option.

 The case sits at an angle which was very important to me. I hope it does not mess anything up as I spent a lot on it.

![image of the CAD model I spent 10 minutes importing](<Screenshot 2026-09-23 165755.png>)

 Made in Tinkercad(which I will hopefully not touch with a 10 meter pole for a while) cause my laptop decided that Fusion360 isn't necesarry and I am demanding too much.

 ## Schematic:
 This is the schematic which didn't come with too may issues unlike last time I tried(and failed) to build for Hackpad.

![schematic](<Screenshot 2026-09-25 000948.png>)

## PCB:
With the PCB the issue was spacing the keycaps mostly and almost getting the direction of the OLED wrong but the rest was fine honestly(again way better than last time).

NOTE: Just noticed the OLED is wrong in this image too. I will change it when I can.

![PCB](<Screenshot 2026-09-19 183047.png>)

## Frimware overview:
It uses KMK for everything.

It has a rotary encoder that controls the volume and mode as stated before, 9 keys with shortcuts depending on the mode and an OLED for showing the current mode which I will have to spice up ASAP.

## BOM:
List of part:

Seeed Studio XIAO Microcontroller
0.91" 128x32 I2C OLED Display (SSD1306)
EC11 Rotary Encoder with Push Button
Mechanical Key Switches (x9)
1U Keycaps (x9)
Custom PCB
3D Printed case
1N4148 Signal Diodes (x10)
LEDs (x10)

## Extra stuff:
I just had a heart attack cause my firmware was from one year ago, all of it but luckly I think I found the right one. Fingers crossed.
This was really fun(excluding the loosing the firmare at midnight) anyways hope you have a great day/evening/night!



