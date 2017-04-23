import unittest

import mock

import influx_metrics


class TestInfluxMetrics(unittest.TestCase):
    def setUp(self):
        self.influx_metrics = influx_metrics.InfluxMetrics(
            "https://influxdb.example.com:8086/write?db=data",
            False, "admin", "monkey123"
        )

    @mock.patch('requests.post')
    def test_report(self, mock_post):
        self.influx_metrics.report(58, True)

        self.assertEqual(mock_post.call_count, 2)

        call1 = mock_post.call_args_list[0]
        self.assertEqual(call1[0], ("https://influxdb.example.com:8086/write?db=data",))
        self.assertEqual(call1[1]["data"], "temp value=58")
        self.assertEqual(call1[1]["auth"].username, "admin")
        self.assertEqual(call1[1]["auth"].password, "monkey123")
        self.assertFalse(call1[1]["verify"])

        call2 = mock_post.call_args_list[1]
        self.assertEqual(call2[0], ("https://influxdb.example.com:8086/write?db=data",))
        self.assertEqual(call2[1]["data"], "heat value=1")
        self.assertEqual(call2[1]["auth"].username, "admin")
        self.assertEqual(call2[1]["auth"].password, "monkey123")
        self.assertFalse(call2[1]["verify"])

    @mock.patch('influx_metrics.print')
    @mock.patch('requests.post')
    def test_does_not_raise(self, mock_post, mock_print):
        mock_post.side_effect = RuntimeError("403 or something")

        self.influx_metrics.report(58, True)

        self.assertEqual(mock_post.call_count, 2)
