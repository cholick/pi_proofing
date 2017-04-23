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
