"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from .config_groups import MagnetSensorConfigs
from .config_groups import MountPoseConfigs
from .config_groups import GyroTrimConfigs
from .config_groups import Pigeon2FeaturesConfigs
from .config_groups import MotorOutputConfigs
from .config_groups import CurrentLimitsConfigs
from .config_groups import VoltageConfigs
from .config_groups import TorqueCurrentConfigs
from .config_groups import FeedbackConfigs
from .config_groups import DifferentialSensorsConfigs
from .config_groups import DifferentialConstantsConfigs
from .config_groups import OpenLoopRampsConfigs
from .config_groups import ClosedLoopRampsConfigs
from .config_groups import HardwareLimitSwitchConfigs
from .config_groups import AudioConfigs
from .config_groups import SoftwareLimitSwitchConfigs
from .config_groups import MotionMagicConfigs
from .config_groups import CustomParamsConfigs
from .config_groups import ClosedLoopGeneralConfigs
from .config_groups import Slot0Configs
from .config_groups import Slot1Configs
from .config_groups import Slot2Configs
from .config_groups import SlotConfigs
from .talon_fx_configs import TalonFXConfiguration, TalonFXConfigurator
from .cancoder_configs import CANcoderConfiguration, CANcoderConfigurator
from .pigeon2_configs import Pigeon2Configuration, Pigeon2Configurator


__all__ = [
    "MagnetSensorConfigs",
    "MountPoseConfigs",
    "GyroTrimConfigs",
    "Pigeon2FeaturesConfigs",
    "MotorOutputConfigs",
    "CurrentLimitsConfigs",
    "VoltageConfigs",
    "TorqueCurrentConfigs",
    "FeedbackConfigs",
    "DifferentialSensorsConfigs",
    "DifferentialConstantsConfigs",
    "OpenLoopRampsConfigs",
    "ClosedLoopRampsConfigs",
    "HardwareLimitSwitchConfigs",
    "AudioConfigs",
    "SoftwareLimitSwitchConfigs",
    "MotionMagicConfigs",
    "CustomParamsConfigs",
    "ClosedLoopGeneralConfigs",
    "Slot0Configs",
    "Slot1Configs",
    "Slot2Configs",
    "SlotConfigs",
    "TalonFXConfiguration",
    "TalonFXConfigurator",
    "CANcoderConfiguration",
    "CANcoderConfigurator",
    "Pigeon2Configuration",
    "Pigeon2Configurator",
]
