from commands2 import SubsystemBase
from hal import SerialPort
from ntcore import NetworkTableInstance
from wpilib import Field2d, RobotBase, RobotState, SmartDashboard, Timer
from wpimath.kinematics import (
    SwerveModulePosition,
    SwerveModuleState,
    SwerveDrive4Kinematics,
)
from wpimath.estimator import SwerveDrive4PoseEstimator
from wpimath.controller import HolonomicDriveController, PIDController
from wpimath.geometry import Translation2d, Rotation2d, Pose2d
from wpimath.filter import SlewRateLimiter
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

        self.odometry = SwerveDrive4PoseEstimator(
            self.kinematics,
            self.gyro.getRotation2d(),
            [
                self.fl.getPosition(),
                self.fr.getPosition(),
                self.bl.getPosition(),
                self.br.getPosition(),
            ],
            Pose2d(Translation2d(), Rotation2d().fromDegrees(0)),
        )

        xPID = PIDController(0.5, 0.0, 0.0)
        xPID.setTolerance(0.05)
        xPID.reset()

        yPID = PIDController(0.5, 0.0, 0.0)
        yPID.setTolerance(0.05)
        yPID.reset()

        tPID = PIDController(0.5, 0.0, 0.0)
        tPID.setTolerance(0.05)
        tPID.reset()

        tPID.enableContinuousInput(-math.pi, math.pi)
        tPID.setTolerance(math.pi / 16)
        tPID.reset(self.getRobotAngle().radians())

        self.holonomic_PID = HolonomicDriveController(xPID, yPID, tPID)

        self.x_limiter = SlewRateLimiter(1)
        self.y_limiter = SlewRateLimiter(1)
        self.t_limiter = SlewRateLimiter(1)

        SmartDashboard.putData("Field", Field2d())

    def periodic(self):
        pose = self.odometry.updateWithTime(
            Timer.getFPGATimestamp(),
            self.gyro.getRotation2d(),
            [
                self.fl.getPosition(),
                self.fr.getPosition(),
                self.bl.getPosition(),
                self.br.getPosition(),
            ],
        )

        poseX = round(pose.X(), 3)
        poseY = round(pose.Y(), 3)
        poseT = round(pose.rotation().degrees(), 3)

        self.__ntTbl__.putNumber("PositionX", poseX)
        self.__ntTbl__.putNumber("PositionY", poseY)
        self.__ntTbl__.putNumber("Rotation", poseT)
