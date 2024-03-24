from commands2 import InstantCommand, SubsystemBase
from hal import SerialPort
from ntcore import NetworkTableInstance
from wpilib import DriverStation, Field2d, RobotBase, RobotState, SmartDashboard, Timer
from wpimath.kinematics import (
    SwerveModulePosition,
    SwerveModuleState,
    SwerveDrive4Kinematics,
    ChassisSpeeds,
)
from wpimath.estimator import SwerveDrive4PoseEstimator
from wpimath.controller import HolonomicDriveController, PIDController
from wpimath.geometry import Translation2d, Rotation2d, Pose2d
from wpimath.filter import SlewRateLimiter
from wpiutil import *
from navx import AHRS
import math
from wpimath.units import feetToMeters

import swerve_module

# MPS
maxVelocity = feetToMeters(15)
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

        if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
            poseX = 16.523 - poseX
            poseY = 8.013 - poseY
            poseT -= 180

        SmartDashboard.putNumberArray(f"Field\{self.robotName}", [poseX, poseY, poseT])

    def stop(self):
        self.runChassisSpeeds(ChassisSpeeds(0, 0, 0))

    ## gets
    def get_holonomicPID(self) -> HolonomicDriveController:
        return self.holonomic_PID

    def get_kinematics(self) -> SwerveDrive4Kinematics:
        return self.kinematics

    def get_odometry(self) -> SwerveDrive4PoseEstimator:
        return self.odometry

    def get_pose(self) -> Pose2d:
        return self.odometry.getEstimatedPosition()

    def get_angle(self) -> Rotation2d:
        return self.gyro.getRotation2d()

    def get_field_relative(self):
        return self.fieldRelative

    def set_field_relative(self, new_val: bool):
        self.fieldRelative.set(new_val)

    def set_field_relative_command(self, new_val: bool) -> InstantCommand:
        cmd = InstantCommand(lambda: self.set_field_relative(new_val), self)
        cmd.runsWhenDisabled = True
        return cmd

    def reset_gyro(self, new_val: Rotation2d = Rotation2d(0)) -> None:
        self.gyro.reset(new_val)

    def reset_gyro_command(self, new_val: Rotation2d = Rotation2d(0)) -> InstantCommand:
        cmd = InstantCommand(lambda: self.reset_gyro(), self)
        cmd.runsWhenDisabled = True
        return cmd

    def set_drive_idle(self, coast: bool):
        self.fl.set_drive_idle(coast)
        self.fr.set_drive_idle(coast)
        self.bl.set_drive_idle(coast)
        self.br.set_drive_idle(coast)

    def set_drive_idle_command(self, coast: bool):
        cmd = InstantCommand(lambda: self.set_drive_idle(coast), self)
        cmd.runsWhenDisabled = True
        return cmd

    def set_drive_idle(self, coast: bool):
        self.fl.set_turn_idle(coast)
        self.fr.set_turn_idle(coast)
        self.bl.set_turn_idle(coast)
        self.br.set_turn_idle(coast)

    def set_turn_idle_command(self, coast: bool):
        cmd = InstantCommand(lambda: self.set_turn_idle(coast), self)
        cmd.runsWhenDisabled = True
        return cmd

    def set_max_speed(self, speed: float) -> None:
        global maxVelocity
        maxVelocity = speed

    def set_max_speed_command(self, speed: float) -> InstantCommand:
        return InstantCommand(lambda: self.set_max_speed(speed), self)

    ## drive
    def run_percentage(
        self, x: float = 0.0, y: float = 0.0, theta: float = 0.0
    ) -> None:
        vX = self.x_limiter.calculate(x * maxVelocity)
        vY = self.y_limiter.calculate(y * maxVelocity)
        vT = self.t_limiter.calculate(theta * maxAnglularVelocity)

        if self.get_field_relative():
            speeds = ChassisSpeeds.fromFieldRelativeSpeeds(
                vx=vX, vy=vY, omega=vT, robotAngle=self.get_angle()
            )
        else:
            speeds = ChassisSpeeds(vx=vX, vy=vY, omega=vT)

        self.holonomic_PID.getThetaController().reset(self.get_angle().radians(), vT)

        self.run_chassis_speeds(speeds)

    def run_chassis_speeds(
        self,
        speeds: ChassisSpeeds,
        center_of_rotation: Translation2d = Translation2d(0, 0),
    ) -> None:
        if self.get_field_relative():
            speeds = ChassisSpeeds.fromFieldRelativeSpeeds(speeds, self.get_angle())

        states = self.kinematics.toSwerveModuleStates(speeds, center_of_rotation)

        self.run_module_states(list(states))

    def run_module_states(self, states) -> None:
        states = self.kinematics.desaturateWheelSpeeds(states, maxVelocity)
        self.fl.setDesiredState(states[0])
        self.fr.setDesiredState(states[1])
        self.bl.setDesiredState(states[2])
        self.br.setDesiredState(states[3])
