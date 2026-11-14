
import unittest

from algorithms.fcfs import fcfs
from algorithms.sstf import sstf
from algorithms.scan import scan
from utils.validation import parse_inputs


class TestDiskScheduling(unittest.TestCase):

    # TEST 1: FCFS preserves original queue order
    def test_fcfs_order(self):
        result = fcfs(50, [90, 20, 70])

        self.assertEqual(
            result["sequence"],
            [90, 20, 70]
        )

        self.assertEqual(
            result["total_movement"],
            160
        )

    # TEST 2: SSTF selects the nearest request
    def test_sstf_nearest_request(self):
        result = sstf(50, [90, 20, 70])

        self.assertEqual(
            result["sequence"],
            [70, 90, 20]
        )

        self.assertEqual(
            result["total_movement"],
            110
        )

    # TEST 3: SCAN moving RIGHT
    def test_scan_right(self):
        result = scan(
            100,
            [150, 300, 50, 20],
            0,
            499,
            "right"
        )

        self.assertEqual(
            result["sequence"],
            [150, 300, 499, 50, 20]
        )

        self.assertEqual(
            result["total_movement"],
            878
        )

    # TEST 4: SCAN moving LEFT
    def test_scan_left(self):
        result = scan(
            100,
            [50, 20, 150, 180],
            0,
            199,
            "left"
        )

        self.assertEqual(
            result["sequence"],
            [50, 20, 0, 150, 180]
        )

        self.assertEqual(
            result["total_movement"],
            280
        )

    # TEST 5: Dynamic maximum cylinder
    def test_custom_maximum(self):
        result = scan(
            100,
            [150, 300],
            0,
            499,
            "right"
        )

        self.assertEqual(
            result["sequence"],
            [150, 300, 499]
        )

        self.assertEqual(
            result["total_movement"],
            399
        )

    # TEST 6: Duplicate requests
    def test_duplicate_requests(self):
        result = fcfs(50, [70, 70, 20])

        self.assertEqual(
            result["sequence"],
            [70, 70, 20]
        )

        self.assertEqual(
            result["total_movement"],
            70
        )

    # TEST 7: Empty request queue
    def test_empty_queue(self):
        with self.assertRaises(ValueError):
            parse_inputs("50", "", "0", "199", "right")

    # TEST 8: Invalid disk range
    def test_invalid_disk_range(self):
        with self.assertRaises(ValueError):
            parse_inputs("50", "70, 80", "199", "0", "right")

    # TEST 9: Head below minimum
    def test_head_below_minimum(self):
        with self.assertRaises(ValueError):
            parse_inputs("-1", "50, 70", "0", "199", "right")

    # TEST 10: Head above maximum
    def test_head_above_maximum(self):
        with self.assertRaises(ValueError):
            parse_inputs("200", "50, 70", "0", "199", "right")

    # TEST 11: Request outside disk range
    def test_request_outside_range(self):
        with self.assertRaises(ValueError):
            parse_inputs("50", "70, 250", "0", "199", "right")

    # TEST 12: Invalid SCAN direction
    def test_invalid_direction(self):
        with self.assertRaises(ValueError):
            parse_inputs("50", "70, 80", "0", "199", "up")

    
    # TEST 13: SCAN explanation details
    def test_scan_explanation(self):

        result = scan(
            100,
            [150, 300, 50, 20],
            0,
            499,
            "right"
        )

        details = result["scan_details"]

        self.assertEqual(
            details["initial_direction"],
            "right"
        )

        self.assertEqual(
            details["boundary"],
            499
        )

        self.assertEqual(
            details["reversed_at"],
            499
        )

        self.assertTrue(
            len(details["events"]) >= 3
        )
        
if __name__ == "__main__":
    unittest.main(verbosity=2)
