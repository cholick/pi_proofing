import RPi.GPIO as gpio


class HeaterSwitch():
    def __init__(self, pin):
        self.pin = pin
        self.on = False
        gpio.setmode(gpio.BCM)

    def toggle(self):
        gpio.setup(self.pin, gpio.OUT)
        if self.on:
            self.turn_off()
        else:
            self.turn_on()

    def turn_on(self):
        self.on = True
        gpio.output(self.pin, gpio.HIGH)

    def turn_off(self):
        self.on = False
        gpio.output(self.pin, gpio.LOW)
