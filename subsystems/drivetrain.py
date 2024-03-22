from commands2 import SubsystemBase
from hal import SerialPort
from ntcore import NetworkTableInstance
from wpilib import RobotBase, RobotState, SmartDashboard
from wpimath.kinematics import (
    SwerveModulePosition,
    SwerveModuleState,
    SwerveDrive4Kinematics,
)
from wpimath.controller import HolonomicDriveController
from wpimath.geometry import Translation2d, Rotation2d
from wpiutil import *
from navx import AHRS
import math
import swerve_module

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

    def __init__(self):
        super().__init__()
        self.subsystem("Drivetrain")
        self.setName("Drivetrain")

        self.robotName = "Robot"
        self.gyro = AHRS(serial_port_id=SerialPort.USB1)

        self.fl = swerve_module.SwerveModule("fl", 14, 12, 13, True, True)
        self.fr = swerve_module.SwerveModule("fr", 11, 9, 10, False, True)
        self.bl = swerve_module.SwerveModule("bl", 17, 15, 16, True, True)
        self.br = swerve_module.SwerveModule("br", 8, 6, 7, False, True)

        self.addChild("Gryo", self.gyro)

        self.kinematics = SwerveDrive4Kinematics(
            self.fl.getModulePosition(),
            self.fr.getModulePosition(),
            self.bl.getModulePosition(),
            self.br.getModulePosition(),
        )
