"""
Utility functions in Phoenix 6
"""

"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.phoenix_native import Native


def get_current_time_seconds() -> float:
    """
    Get the current timestamp in seconds.

    This will return the current time in seconds, this is
    the same time that is used in Timestamp.
    :returns: Current time in seconds
    :rtype: float
    """
    return Native.instance().c_ctre_phoenix6_get_current_time_seconds()


def is_simulation() -> bool:
    """
    Get whether the program is running in simulation.

    :returns: True if in simulation
    :rtype: bool
    """
    return Native.instance().c_ctre_phoenix6_is_simulation()
