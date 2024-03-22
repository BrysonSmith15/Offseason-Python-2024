from commands2 import SubsystemBase
from ntcore import NetworkTableInstance
from wpilib import RobotBase, RobotState, SmartDashboard
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState
from wpimath.controller import HolonomicDriveController
from wpimath.geometry import Translation2d, Rotation2d
from wpiutil import *
from navx import AHRS
import math

# MPS
maxVelocity = 3.7
# RAD / S
maxAnglularVelocity = 1 * math.pi


class Drivetrain(SubsystemBase):
    class BooleanProperty:
        _name: str = ""
        _value: bool = False

        def __init__(self, name: str, value: bool = False):
            self._name = name
            self.set(value)

        def set(self, value: bool) -> None:
            self._value = value
            SmartDashboard.putBoolean(self._name, self._value)

        def get(self) -> None:
            return self._value

        def toggle(self) -> None:
            self.set(not self._value)

    __ntTbl__ = NetworkTableInstance.getDefault().getTable("Drivetrain")
    fieldRelative: BooleanProperty = BooleanProperty("fieldRelative", True)
    holonomic_PID: HolonomicDriveController = None
