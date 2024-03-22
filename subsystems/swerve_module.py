"""
Description: Swerve Module (Swerve Drive Specialites mk4)
Version: 1
Date: 3/21/24

Drive Motor Controllers: Spark MAX
Turn Motor Controllers: Spark MAX
Angle Sensors: CANCoder (turn), Neo integrated (drive)

Velocity Controller: Closed Loop (Spark Integrated)
Angle Controller: Closed Loop (WPILib)
"""

import math

from commands2 import SubsystemBase
from phoenix6.hardware import CANcoder
from rev import CANSparkMax, CANSparkLowLevel, SparkRelativeEncoder
from wpilib import RobotBase, RobotState
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState
from wpimath.geometry import Translation2d, Rotation2d
from wpiutil import *

# consts

drive_P = 0.04
drive_I = 0.0
drive_D = 0.0
drive_MaxVel_MM = 20480


turn_P = 6e-1
turn_I = 0.0
turn_D = 0.0


class SwerveModule(SubsystemBase):
    motion_magic: bool = False

    drive_motor: CANSparkMax = None
    turn_motor: CANSparkMax = None
    cancoder: CANcoder = None
    drive_encoder: SparkRelativeEncoder = None
    turn_encoder: SparkRelativeEncoder = None
    module_position: Translation2d = None
    module_state: SwerveModuleState = None

    def __init__(
        self,
        subsystem_name: str,
        drive_id: int,
        turn_id: int,
        encoder_id: int,
        turn_inverted: bool,
        drive_inverted: bool,
    ):
        self.cancoder = CANcoder(encoder_id)
        self.turn_motor = CANSparkMax(turn_id, CANSparkLowLevel.MotorType.kBrushless)
        self.drive_motor = CANSparkMax(drive_id, CANSparkLowLevel.MotorType.kBrushless)

        self.cancoder.setPosition(self.encoder.getAbsolutePosition())

        self.turn_encoder = self.turn_motor.getEncoder()
        self.turn_encoder.setPosition(
            self.cancoder.getAbsolutePosition().GetValue() / 360.0
        )
        self.turn_encoder.setPositionConversionFactor(1 / 12.8)
        self.turn_encoder.setVelocityConversionFactor(1 / 12.8)

        self.turn_motor.setInverted(turn_inverted)
        self.turn_motor.getPIDController().setFeedbackDevice(self.turn_encoder)
        self.turn_motor.getPIDController().setP(turn_P)
        self.turn_motor.getPIDController().setI(turn_I)
        self.turn_motor.getPIDController().setD(turn_D)

        self.drive_encoder.setPosition(0)
        self.drive_encoder.setPositionConversionFactor(1 / 8.14)
        self.drive_encoder.setVelocityConversionFactor(1 / 8.14)

        self.drive_motor.getPIDController().setP(drive_P)
        self.drive_motor.getPIDController().setI(drive_I)
        self.drive_motor.getPIDController().setD(drive_D)
        self.drive_motor.getPIDController().setFeedbackDevice(self.drive_encoder)
        self.drive_motor.setInverted(drive_inverted)

        self.setSubsytem(f"SwerveModule/{subsystem_name}")
        self.setName(f"SwerveModule/{subsystem_name}")
        self.add_child("Drive", self.drive_motor)
        self.add_child("Turn", self.turn_motor)
        self.add_child("Drive Sensor", self.drive_encoder)
        self.add_child("Turn Sensor", self.turn_encoder)

        self.module_state = SwerveModuleState(0, Rotation2d(0))

        def periodic(self) -> None:
            pass

        def setDesiredState(self, desiredState: SwerveModuleState):
            currAnglePos = self.turn_encoder.getPosition()
            currAngleRotation = Rotation2d(0).fromDegrees(currAnglePos)
            optimalState: SwerveModuleState = SwerveModuleState.optimize(
                desiredState, currAngleRotation
            )
            self.module_state = optimalState

            velocity = optimalState.speed
            self.drive_motor.set(CANSparkLowLevel.ControlType.kVelocity, velocity)
            self.turn_motor.set(
                CANSparkLowLevel.ControlType.kPosition, optimalState.angle.degrees / 180
            )


m = SwerveModule("a", 1, 1, 1, 1, 1, 1)
m.setDesiredState()
