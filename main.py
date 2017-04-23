#!/usr/bin/env python2
import os
import sys

from proofing import config, heater_switch, temp_sensor, habitat

PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(PATH, 'lib'))


def main():
    # import proofing.config
    conf = config.Config()
    sensor = temp_sensor.TempSensor(conf.serial)
    switch = heater_switch.HeaterSwitch(conf.switch_pin)

    hab = habitat.Habitat(conf, sensor, switch)
    hab.maintain()


if __name__ == "__main__":
    main()
