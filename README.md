# afks-pi-pico-party-lights

This repo contains the code used in my Raspberry Pi Pico RGB party lights project showcased in my latest *afk steph* YouTube video: [every developer should try this](https://youtu.be/-kyYm0ubKPQ).

![alt text](https://github.com/afksteph/afks-pi-pico-party-lights/blob/main/pico_party_lights.jpg)

## Overview

The aim of this project was to build a Raspberry Pi Pico 'RGB party light device' through the use of a Little Bird Lorikeet LED stick, as well as a button for toggling light modes and a potentiometer for modifying the speed.

Guides referenced:
- [Get Started with MicroPython on Raspberry Pi Pico](https://core-electronics.com.au/get-started-with-micropython-on-raspberry-pi-pico.html)
  - Although this is now outdated, see the [2nd edition](https://raspberry.piaustralia.com.au/products/get-started-with-micropython-on-raspberry-pi-pico-2nd-edition) or [online docs](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico) for getting started with a Pico :)
- [Raspberry Pi Pico with Lorikeet WS2812B LED Stick](https://learn.littlebirdelectronics.com.au/guides/raspberry-pi-with-lorikeet-ws2812b-led-stick)

## Requirements

All electronics used for this project came from: [Electronics Kit for Raspberry Pi Pico](https://raspberry.piaustralia.com.au/products/electronics-kit-for-raspberry-pi-pico).
- Raspberry Pi Pico
- Momentary Pushbutton Switch - 12mm Square (aka the button)
- Trimpot 10K with Knob (aka the potentiometer)
- Little Bird Lorikeet (aka the programmable RGB lights)
- Breadboard
- Jumper wires

For programming the Lorikeet RGB lights, the Neopixel library needs to saved to the Pico. See the [pi_pico_neopixel](https://github.com/blaz-r/pi_pico_neopixel) repo for more information.

## Usage

See the getting started guides mentioned above for guidance around running a Micropython file on the Pico.

For the code files to run as-is, it is assumed that the Pico is connected to the electronic components via the following GPIO pins:
- Lorikeet - pin 38
- Potentiometer - pin 26
- Button - pin 27 (only required for party_light_mvp.py)

Both files involve toggling between the following party light modes (most of this code was copied from the Neopixel repo examples folder):
- Inactive
- Color Wave
- Smooth Rainbow
- Fireflies
- Blue Strobe

### party_light_mvp.py

This code is mentioned in the YouTube video at timestamp: 13:12.

This file is named 'mvp' due to the fact that it has bad code quality and was simply written to get my project to work. I intended to refactor and improve this, but I lost my button component so would not have been able to test it, so I've decided to just leave it as is. It's amusing to look back on I suppose haha.

The expected behaviour upon running this code is that pressing the button will toggle the different light modes to display on the Lorikeet and adjusting the potentiometer will increase or decrease the speed of the current light mode's iterations through colours/strobes/flashing.

### party_light_final_but_no_button.py

This code is mentioned in the YouTube video at timestamp: 14:23.

This file is an attempt at refactoring party_light_mvp.py with better code quality and implemented a simple factory pattern class structure for the light modes. However, as I lost/misplaced the button component, this implementation's logic is slightly different to the original mvp file.

The expected behaviour upon running this code is that adjusting the potentiometer knob will execute the toggling between light modes. The light flashing speed is left constant.

### Reference Diagram

> If You can even call this a 'diagram'...

![alt text](https://github.com/afksteph/afks-pi-pico-party-lights/blob/main/original_project_idea_rough_diagram.png)

I created this rough diagram in PowerPoint (lol, can you tell I am complete beginner to the world and electronics?) ((if anyone has suggestions/recommendations on where to learn to do this kind of thing the 'proper' way, hmu))

My original grand epic idea involved also using the mini photo cell as a light sensor to automatically turn the party light device on or off... However, I realised I didn't have enough wires to make this work with the single breadboard, so I never ended up including the mini photo cell componenet. Maybe one day...