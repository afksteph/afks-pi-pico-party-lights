import time
from neopixel import Neopixel
import machine
from utime import sleep
import random


print("Party timeeeee yipeeee!")


class Config:
    pin = 28
    numpix = 30
    colors = [
        (255, 0, 0),  # red
        (255, 50, 0),  # orange
        (255, 100, 0),  # yellow
        (0, 255, 0),  # green
        (0, 0, 255),  # blue
        (100, 0, 90),  # indigo
        (200, 0, 100),  # violet
    ]


class LightMode:
    
    def activate(self, strip):
        raise NotImplemented

    def run(self, strip):
        raise NotImplemented


class InactiveLightMode(LightMode):
    def activate(self, strip):
        strip.clear()
        strip.show()

    def run(self, strip):
        pass


class ColorWaveLightMode(LightMode):
    def __init__(self):
        self.step = round(Config.numpix / len(Config.colors))

    
    def activate(self, strip):
        current_pixel = 0
        for color1, color2 in zip(Config.colors, Config.colors[1:]):
            strip.set_pixel_line_gradient(current_pixel, current_pixel + self.step, color1, color2)
            current_pixel += self.step
        strip.set_pixel_line_gradient(current_pixel, Config.numpix - 1, Config.colors[6], Config.colors[1])
        strip.show()

    def run(self, strip):
        strip.rotate_right(1)
        strip.show()


class SmoothRainbowLightMode(LightMode):
    def __init__(self):
        self.hue = 0

    def activate(self, strip):
        pass

    def run(self, strip):
        color = strip.colorHSV(self.hue, 255, 150)
        strip.fill(color)
        strip.show()
        self.hue += 150


class FirefliesLightMode(LightMode):
    def __init__(self):
        self.max_len = 20
        self.min_len = 5
        self.num_flashes = 10
        self.flashing = []
        self._set_up()

    def _set_up(self):
        for i in range(self.num_flashes):
            pix = random.randint(0, Config.numpix - 1)
            col = random.randint(1, len(Config.colors) - 1)
            flash_len = random.randint(self.min_len, self.max_len)
            self.flashing.append([pix, Config.colors[col], flash_len, 0, 1])

    def activate(self, strip):
        strip.fill((0,0,0))
        strip.show()

    def run(self, strip):
        for i in range(self.num_flashes):
            pix = self.flashing[i][0]
            brightness = (self.flashing[i][3]/self.flashing[i][2])
            colr = (int(self.flashing[i][1][0]*brightness), 
                    int(self.flashing[i][1][1]*brightness), 
                    int(self.flashing[i][1][2]*brightness))
            strip.set_pixel(pix, colr)

            if self.flashing[i][2] == self.flashing[i][3]:
                self.flashing[i][4] = -1
            if self.flashing[i][3] == 0 and self.flashing[i][4] == -1:
                pix = random.randint(0, Config.numpix - 1)
                col = random.randint(0, len(Config.colors) - 1)
                flash_len = random.randint(self.min_len, self.max_len)
                self.flashing[i] = [pix, Config.colors[col], flash_len, 0, 1]
            self.flashing[i][3] = self.flashing[i][3] + self.flashing[i][4]
        strip.show()


class BlueStrobeLightMode(LightMode):
    def __init__(self):
        self.brightness = 0
        self.brightness_increasing = True

    def activate(self, strip):
        strip.fill((0, 0, 255), self.brightness)
        strip.show()

    def run(self, strip):
        if self.brightness_increasing:
            self.brightness = self.brightness + 5
        else:
            self.brightness = self.brightness - 5

        if self.brightness == 0 or self.brightness == 255:
            self.brightness_increasing = not self.brightness_increasing

        strip.fill((0, 0, 255), self.brightness)
        strip.show()


strip = Neopixel(Config.numpix, 0, Config.pin, "GRB")
strip.brightness(50)
light_modes = {
    0: InactiveLightMode(),
    1: ColorWaveLightMode(),
    2: SmoothRainbowLightMode(),
    3: FirefliesLightMode(),
    4: BlueStrobeLightMode()
}
potentiometer = machine.ADC(26)
conversion_factor = (len(light_modes) - 1) / 65535
curr_mode = 0
prev_mode = 0

while True:
    try:
        # Potentiometer readings will return a curr_mode value ranging from 0 to 4
        curr_mode = round(potentiometer.read_u16() * conversion_factor)
        if prev_mode != curr_mode:
            print(f"Light mode updated! {curr_mode}")
            prev_mode = curr_mode
            light_modes[curr_mode].activate(strip)
        light_modes[curr_mode].run(strip)
        time.sleep(0.01)
    except KeyboardInterrupt:
        break

light_modes[0].activate(strip)

print("Finished.")