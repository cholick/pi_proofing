import unittest

import mock

import config


class TestConfig(unittest.TestCase):
    def test_constructor(self):
        file_contents = """{
  "serial": "28-000000aaaaaa",
  "switchPin": 14,
  "temp": 85
}"""

        my_mock_open = mock.mock_open(read_data=file_contents.strip())
        with mock.patch('config.open', my_mock_open):
            my_config = config.Config()

        self.assertEqual(my_config.serial, "28-000000aaaaaa")
        self.assertEqual(my_config.switch_pin, 14)
        self.assertEqual(my_config.temp, 85)
        self.assertIsNone(my_config.influx_url)

    def test_optionally_adds_influx(self):
        file_contents = """{
          "serial": "28-000000aaaaaa",
          "switchPin": 14,
          "temp": 85,
          "influxURL": "https://influxdb.example.com:8086/write?db=data",
          "influxValidateSSL": false,
          "influxUser": "admin",
          "influxPassword": "monkey123"
        }"""

        my_mock_open = mock.mock_open(read_data=file_contents.strip())
        with mock.patch('config.open', my_mock_open):
            my_config = config.Config()

        self.assertEqual(my_config.influx_url, "https://influxdb.example.com:8086/write?db=data")
        self.assertFalse(my_config.influx_validate_ssl)
        self.assertEqual(my_config.influx_user, "admin")
        self.assertEqual(my_config.influx_password, "monkey123")
