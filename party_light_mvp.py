# This is definitely not my best work, but hey, it works!
# Maybe one day I'll replace my lost button component to refactor and test this code.

import time
import gc
from neopixel import Neopixel
import machine
from utime import sleep
import _thread
import random


print("Party timeeeee yipeeee!")

potentiometer = machine.ADC(26)
conversion_factor = 0.05 / (65535)

numpix = 30
strip = Neopixel(numpix, 0, 28, "GRB")
colors = [
    (255, 0, 0),  # red
    (255, 50, 0),  # orange
    (255, 100, 0),  # yellow
    (0, 255, 0),  # green
    (0, 0, 255),  # blue
    (100, 0, 90),  # indigo
    (200, 0, 100),  # violet
]
step = round(numpix / len(colors))
brightness = 50
brightness_increasing = True
strip.brightness(brightness)
hue = 0
max_len=20
min_len = 5
flashing = []
num_flashes = 10

for i in range(num_flashes):
    pix = random.randint(0, numpix - 1)
    col = random.randint(1, len(colors) - 1)
    flash_len = random.randint(min_len, max_len)
    flashing.append([pix, colors[col], flash_len, 0, 1])

button = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_pressed = False
mode = 0
prev_button = 0

# I originally tried to use multithreading to help handle the check button press logic
# and implement toggling between light modes, but I couldn't get it to work, so I ended
# up with the below monstrosity instead.
while True:
    try:
        if button.value() == 1:
            if prev_button == 0:  # Toggle to the light mode
                print(f"Button pressed! mode: {mode}")
                mode = (mode + 1) % 5
                print(f"New mode: {mode}")
                if mode == 0:
                    strip.clear()
                    strip.show()
                elif mode == 1: # color wave
                    current_pixel = 0
                    for color1, color2 in zip(colors, colors[1:]):
                        strip.set_pixel_line_gradient(current_pixel, current_pixel + step, color1, color2)
                        current_pixel += step
                    strip.set_pixel_line_gradient(current_pixel, numpix - 1, colors[6], colors[1])
                    strip.show()
                elif mode == 2:
                    pass
                elif mode == 3:
                    pass
                elif mode == 4: # blue strobe
                    brightness = 0
                    brightness_increasing = True
                    strip.fill((0, 0, 255), brightness)
                    strip.show()
                prev_button = 1
        elif prev_button == 1:
            prev_button = 0
        if mode == 0:
            pass
        elif mode == 1: # color wave
            strip.rotate_right(1)
            for i in range(numpix):
                pixel = strip.get_pixel(i)
            time.sleep(potentiometer.read_u16() * conversion_factor)
            strip.show()
        elif mode == 2: # smooth rainbow
            color = strip.colorHSV(hue, 255, 150)
            strip.fill(color)
            strip.show()
            hue += 150
            time.sleep(potentiometer.read_u16() * conversion_factor)
        elif mode == 3: # fireflies
            for i in range(num_flashes):
                pix = flashing[i][0]
                brightness = (flashing[i][3]/flashing[i][2])
                colr = (int(flashing[i][1][0]*brightness), 
                        int(flashing[i][1][1]*brightness), 
                        int(flashing[i][1][2]*brightness))
                strip.set_pixel(pix, colr)

                if flashing[i][2] == flashing[i][3]:
                    flashing[i][4] = -1
                if flashing[i][3] == 0 and flashing[i][4] == -1:
                    pix = random.randint(0, numpix - 1)
                    col = random.randint(0, len(colors) - 1)
                    flash_len = random.randint(min_len, max_len)
                    flashing[i] = [pix, colors[col], flash_len, 0, 1]
                flashing[i][3] = flashing[i][3] + flashing[i][4]
                time.sleep(potentiometer.read_u16() * conversion_factor)
            strip.show()
        elif mode == 4: # blue strobe
            if brightness_increasing == False:
                brightness = brightness - 5
                if brightness == 0:
                    brightness_increasing = True
            else:
                brightness = brightness + 5
                if brightness == 255:
                    brightness_increasing = False
            print(brightness)
            strip.fill((0, 0, 255), brightness)
            strip.show()
            time.sleep(potentiometer.read_u16() * conversion_factor)
    except KeyboardInterrupt:
        break

strip.clear()
strip.show()
gc.collect()
print("Finished.")