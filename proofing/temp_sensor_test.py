import unittest

import mock

import temp_sensor


class TestTemp(unittest.TestCase):
    def setUp(self):
        self.tempSensor = temp_sensor.TempSensor("28-000000aaaaaa")

    def test_conversion(self):
        self.assertEqual(temp_sensor.celsius_to_fahrenheit_temp(0), 32)
        self.assertEqual(temp_sensor.celsius_to_fahrenheit_temp(51), 123.8)
        self.assertEqual(temp_sensor.celsius_to_fahrenheit_temp(100), 212)

    def test_read_fahrenheit(self):
        file_contents = """
23 01 4b 46 7f ff 0d 10 5c : crc=5c YES
23 01 4b 46 7f ff 0d 10 5c t=18187
"""

        my_mock_open = mock.mock_open(read_data=file_contents.strip())
        with mock.patch('temp_sensor.open', my_mock_open):
            temp = self.tempSensor.read_fahrenheit()

        self.assertAlmostEqual(temp, 64.74, delta=.01)
