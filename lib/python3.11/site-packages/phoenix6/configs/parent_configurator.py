"""
Base class for device configurators
"""

"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.hardware.device_identifier import DeviceIdentifier
from phoenix6.phoenix_native import Native
from phoenix6.status_code import StatusCode
from phoenix6.error_reporting import report_status_code
from phoenix6.units import *
import ctypes

class ParentConfigurator:
    def __init__(self, device_identifier: DeviceIdentifier):
        self.default_timeout_seconds: second = 0.050
        self.__device_identifier = device_identifier

    def _set_configs_private(self, serial_string: str, timeout_seconds: second, future_proof_configs: bool, override_if_duplicate: bool):
        status = StatusCode(Native.instance().c_ctre_phoenix6_set_configs(0,
                                                                          ctypes.c_char_p(bytes(self.__device_identifier.network, encoding='utf-8')),
                                                                          self.__device_identifier.device_hash,
                                                                          timeout_seconds,
                                                                          ctypes.c_char_p(bytes(serial_string, 'utf-8')),
                                                                          len(serial_string),
                                                                          future_proof_configs,
                                                                          override_if_duplicate,
                                                                          False))
        if not status.is_ok():
            location = str(self.__device_identifier) + " Apply Config"
            report_status_code(status, location)
        return status

    def _get_configs_private(self, timeout_seconds: second) -> (StatusCode, str):
        values = ctypes.c_char_p()
        status = StatusCode(Native.instance().c_ctre_phoenix6_get_configs(0,
                                                               ctypes.c_char_p(bytes(self.__device_identifier.network, encoding='utf-8')),
                                                               self.__device_identifier.device_hash,
                                                               timeout_seconds,
                                                               ctypes.byref(values),
                                                               False))
        to_return = ""

        if values.value is not None:
            # Value is not none, so bring it over and free it
            to_return = str(values.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(values))
        if not status.is_ok():
            location = str(self.__device_identifier) + " Refresh Config"
            report_status_code(status, location)
        return (status, to_return)
