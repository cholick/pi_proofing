import unittest

import mock

import config
import habitat
import influx_metrics
import temp_sensor


class TestTemp(unittest.TestCase):
    def setUp(self):
        global counter
        counter = 0

        self.conf = mock.Mock(config.Config)
        self.conf.temp = 81

        self.sensor = mock.Mock(temp_sensor.TempSensor)
        self.swtich = mock.Mock()  # RPi.GPIO fails to import
        self.swtich.on = False

        self.habitat = habitat.Habitat(self.conf, self.sensor, self.swtich)

    @mock.patch('habitat.print')
    @mock.patch('time.sleep')
    def test_sleeps(self, mock_sleep, mock_print):
        def side_effect():
            global counter
            counter += 1
            if counter >= 5:
                self.habitat.run = False
            return 81

        self.sensor.read_fahrenheit.side_effect = side_effect

        self.habitat.maintain()

        self.assertEqual(self.swtich.toggle.call_count, 0)
        self.assertEqual(mock_sleep.call_count, 5)

    @mock.patch('habitat.print')
    @mock.patch('time.sleep')
    def test_toggles_on(self, mock_sleep, mock_print):
        def side_effect():
            global counter
            counter += 1
            if counter >= 5:
                self.habitat.run = False
            if counter == 1:
                return 60
            else:
                return 80

        self.swtich.on = False
        self.sensor.read_fahrenheit.side_effect = side_effect

        self.habitat.maintain()

        self.assertEqual(self.swtich.toggle.call_count, 1)

    @mock.patch('habitat.print')
    @mock.patch('time.sleep')
    def test_toggles_off(self, mock_sleep, mock_print):
        def side_effect():
            global counter
            counter += 1
            if counter >= 5:
                self.habitat.run = False
            if counter == 1:
                return 86
            else:
                return 80

        self.swtich.on = True
        self.sensor.read_fahrenheit.side_effect = side_effect

        self.habitat.maintain()

        self.assertEqual(self.swtich.toggle.call_count, 1)

    @mock.patch('habitat.print')
    @mock.patch('time.sleep')
    def test_bad_reading_failure(self, mock_sleep, mock_print):
        self.sensor.read_fahrenheit.return_value = 32

        self.assertRaises(RuntimeError, self.habitat.maintain)

    @mock.patch('habitat.print')
    @mock.patch('time.sleep')
    def test_reports_metrics(self, mock_sleep, mock_print):
        def side_effect():
            global counter
            counter += 1
            if counter >= 5:
                self.habitat.run = False
            return 60 + counter

        self.sensor.read_fahrenheit.side_effect = side_effect
        metrics = mock.Mock(influx_metrics.InfluxMetrics)
        self.habitat = habitat.Habitat(self.conf, self.sensor, self.swtich, metrics)

        self.habitat.maintain()

        self.assertEqual(metrics.report.call_count, 5)

        call1 = metrics.report.call_args_list[0]
        self.assertEqual(call1[0], (61, False))

        call5 = metrics.report.call_args_list[4]
        self.assertEqual(call5[0], (65, False))
