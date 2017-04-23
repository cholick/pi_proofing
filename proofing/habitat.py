from __future__ import print_function

import time


class Habitat:
    def __init__(self, conf, sensor, switch, metrics=None):
        self.conf = conf
        self.sensor = sensor
        self.switch = switch
        self.metrics = metrics
        self.run = True

    def maintain(self):
        while self.run:
            temp = self.sensor.read_fahrenheit()
            if temp < 50 or temp > 90:
                raise RuntimeError("Sensor failure, temperature reading is {}".format(temp))

            print(temp)

            toggle = False
            if not self.switch.on and temp < self.conf.temp - 4:
                toggle = True
            if self.switch.on and temp > self.conf.temp + 4:
                toggle = True

            if toggle:
                print("Toggling switch from {} to {}".format(self.switch.on, not self.switch.on))
                self.switch.toggle()

            if self.metrics:
                self.metrics.report(temp, self.switch.on)

            time.sleep(2)
