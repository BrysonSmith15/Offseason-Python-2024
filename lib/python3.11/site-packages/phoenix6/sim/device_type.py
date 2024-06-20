"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from enum import Enum


class DeviceType(Enum):
    """
    Enumeration of all supported device types.
    """
    TalonSRXType = 0
    VictorSPXType = 1
    PigeonIMUType = 2
    RibbonPigeonIMUType = 3
    TalonFXType = 4
    CANCoderType = 5
    PRO_TalonFXType = 6
    PRO_CANcoderType = 7
    PRO_Pigeon2Type = 8

