"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.phoenix_native import Native
from phoenix6.status_code import StatusCode
import ctypes


class EmptyControl:
    """
    Generic Empty Control class used to do nothing.
    """

    def __init__(self):
        """
        Constructs an empty control request
        """
        self._name = "EmptyControl"

    @property
    def name(self) -> str:
        """
        Gets the name of this control request.

        :returns: Name of the control request
        :rtype: str
        """
        return self._name

    def __str__(self) -> str:
        return "class: EmptyControl"

    def _send_request(self, network: str, device_hash: int, cancel_other_requests: bool) -> StatusCode:
        return StatusCode(Native.instance().c_ctre_phoenix6_RequestControlEmpty(ctypes.c_char_p(bytes(network, 'utf-8')), device_hash, 0, cancel_other_requests))

    @property
    def control_info(self) -> dict:
        """
        Gets information about this control request.

        :returns: Dictonary of control parameter names and corresponding applied values
        :rtype: dict
        """
        control_info = {}
        control_info["name"] = self._name
        return control_info
