import unittest

from algorithms.fcfs import fcfs
from algorithms.sstf import sstf
from algorithms.scan import scan

from results.formatter import format_result


class TestResultFormatter(unittest.TestCase):

    def test_fcfs_formatter(self):

        result = fcfs(
            53,
            [98, 183, 37, 122, 14, 124, 65, 67]
        )

        formatted = format_result(result, 53)

        self.assertEqual(formatted["total"], 640)
        self.assertEqual(len(formatted["rows"]), 8)
        self.assertTrue(formatted["solution"])

    def test_sstf_formatter(self):

        result = sstf(
            53,
            [98, 183, 37, 122, 14, 124, 65, 67]
        )

        formatted = format_result(result, 53)

        self.assertEqual(formatted["total"], 236)
        self.assertEqual(len(formatted["sstf_steps"]), 8)

    def test_scan_formatter(self):

        result = scan(
            53,
            [98, 183, 37, 122, 14, 124, 65, 67],
            0,
            199,
            "right"
        )

        formatted = format_result(result, 53)

        self.assertEqual(formatted["total"], 331)
        self.assertTrue(formatted["scan_events"])

        self.assertEqual(
            formatted["scan_details"]["boundary"],
            199
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
