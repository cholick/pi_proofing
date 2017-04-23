import re


class TempSensor:
    def __init__(self, serial):
        self.serial = serial

    def read_fahrenheit(self):
        raw_temp = self.__read_raw()
        c_temp = float(raw_temp) / 1000
        return celsius_to_fahrenheit_temp(c_temp)

    def __read_raw(self):
        file_name = '/sys/bus/w1/devices/{}/w1_slave'.format(self.serial)
        with open(file_name) as sensor:
            data = sensor.read()
        match = re.match(r'.*t=(\d+)', data, re.IGNORECASE | re.DOTALL)
        return match.group(1)


def celsius_to_fahrenheit_temp(c_temp):
    return (float(c_temp) * 9 / 5) + 32
