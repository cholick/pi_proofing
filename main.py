import os
import sys
import signal

from proofing import config, habitat, heater_switch, influx_metrics, temp_sensor

PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(PATH, 'lib'))


def handler_stop_signals(signum, frame):
    print "Cleaning up"
    heater_switch.cleanup()
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, handler_stop_signals)
    signal.signal(signal.SIGTERM, handler_stop_signals)

    conf = config.Config()
    sensor = temp_sensor.TempSensor(conf.serial)
    switch = heater_switch.HeaterSwitch(conf.switch_pin)

    metrics = None
    if conf.influx_url:
        metrics = influx_metrics.InfluxMetrics(
            conf.influx_url, conf.influx_validate_ssl, conf.influx_user, conf.influx_password
        )

    hab = habitat.Habitat(conf, sensor, switch, metrics)
    hab.maintain()


if __name__ == "__main__":
    main()
