import RPi.GPIO as gpio


class HeaterSwitch:
    def __init__(self, pin):
        self.pin = pin
        gpio.setmode(gpio.BCM)
        gpio.setup(self.pin, gpio.OUT)

        # start turned off, mitigate previous run cleanup failure
        self.on = False
        self.turn_off()

    def toggle(self):
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


def cleanup():
    gpio.cleanup()
