"""
Functions related to more barebones control of devices,
including manually feeding the enable
"""

"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.phoenix_native import Native
from phoenix6.units import second

def feed_enable(timeout_seconds: second):
    """
    Feeds the enable signal with a timeout specified in seconds

    :param timeout_seconds: Time to remain enabled in seconds
    :type timeout_seconds: second
    """
    Native.instance().c_ctre_phoenix6_unmanaged_feed_enable(int(timeout_seconds * 1000))

def get_api_compliancy() -> int:
    """
    Gets this API's compliancy version

    This is purely used to check compliancy of API against firmware,
    and if there is a mismatch to report to the user.

    :returns: This API's compliancy version
    :rtype: int
    """
    return Native.instance().c_ctre_phoenix6_unmanaged_get_api_compliancy()
