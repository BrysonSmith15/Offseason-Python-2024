"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

"""
Tries various library methods to verify
that library loading is successful
"""

import unittest
import time
from phoenix6.utils import *
from phoenix6.base_status_signal import BaseStatusSignal
from phoenix6.hardware.device_identifier import DeviceIdentifier
from phoenix6.spns.spn_value import SpnValue


class UtilTests(unittest.TestCase):
    def test_get_current_time(self):
        time_1 = get_current_time_seconds()
        time.sleep(0.1)
        time_2 = get_current_time_seconds()
        self.assertNotEqual(time_1, time_2)

    def test_is_simulation(self):
        self.assertFalse(is_simulation())

    def test_units(self):
        tmp = BaseStatusSignal(
            DeviceIdentifier(0, "Talon FX", "Fred"),
            SpnValue.PRO_POS_AND_VEL_POSITION.value,
            "Position",
        )
        self.assertEqual(tmp.units, "rotations")


if __name__ == "__main__":
    unittest.main()
