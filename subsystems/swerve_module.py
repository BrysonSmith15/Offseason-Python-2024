"""
Description: Swerve Module (Swerve Drive Specialties mk4)
Version: 1
Date: 3/21/24

Drive Motor Controllers: Spark MAX
Turn Motor Controllers: Spark MAX
Angle Sensors: CANCoder (turn), Neo integrated (drive)

Velocity Controller: Closed Loop (Spark Integrated)
Angle Controller: Closed Loop (WPILib)
"""

import math

from commands2 import Subsystem
from ntcore import NetworkTableInstance, NetworkTable
from phoenix6.hardware import CANcoder
from rev import CANSparkMax, CANSparkLowLevel, SparkRelativeEncoder
from wpimath import inputModulus
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState
from wpimath.geometry import Translation2d, Rotation2d
from wpimath.units import inchesToMeters


# consts

drive_P = 0.04
drive_I = 0.0
drive_D = 0.0
drive_MaxVel_MM = 20480


turn_P = 6e-1
turn_I = 0.0
turn_D = 0.0


class SwerveModule(Subsystem):
    drive_motor: CANSparkMax = None
    turn_motor: CANSparkMax = None
    cancoder: CANcoder = None
    drive_encoder: SparkRelativeEncoder = None
    turn_encoder: SparkRelativeEncoder = None
    module_position: Translation2d = None
    module_state: SwerveModuleState = None
    network_table: NetworkTable = None

    def __init__(
        self,
        subsystem_name: str,
        drive_id: int,
        turn_id: int,
        encoder_id: int,
        turn_inverted: bool,
        drive_inverted: bool,
    ):
        super().__init__()
        self.name = subsystem_name
        self.network_table = NetworkTableInstance.getDefault().getTable(
            f"Swervemodule/{self.name}"
        )

        self.cancoder = CANcoder(encoder_id)
        self.turn_motor = CANSparkMax(turn_id, CANSparkLowLevel.MotorType.kBrushless)
        self.drive_motor = CANSparkMax(drive_id, CANSparkLowLevel.MotorType.kBrushless)

        self.cancoder.set_position(self.cancoder.get_absolute_position().value)

        self.turn_encoder = self.turn_motor.getEncoder()
        self.turn_encoder.setPosition(
            self.cancoder.get_absolute_position().value / 360.0
        )
        self.turn_encoder.setPositionConversionFactor(1 / 12.8)
        self.turn_encoder.setVelocityConversionFactor(1 / 12.8)

        self.turn_motor.setInverted(turn_inverted)
        self.turn_pid = self.turn_motor.getPIDController()
        self.turn_pid.setFeedbackDevice(self.turn_encoder)
        self.turn_pid.setP(turn_P)
        self.turn_pid.setI(turn_I)
        self.turn_pid.setD(turn_D)

        self.drive_encoder = self.drive_motor.getEncoder()
        self.drive_encoder.setPosition(0)
        self.drive_encoder.setPositionConversionFactor(1 / 8.14)
        self.drive_encoder.setVelocityConversionFactor(1 / 8.14)

        self.drive_pid = self.drive_motor.getPIDController()
        self.drive_pid.setP(drive_P)
        self.drive_pid.setI(drive_I)
        self.drive_pid.setD(drive_D)
        self.drive_pid.setFeedbackDevice(self.drive_encoder)
        self.drive_motor.setInverted(drive_inverted)

        self.setName(f"SwerveModule/{subsystem_name}")

        self.module_state = SwerveModuleState(0, Rotation2d(0))

    def periodic(self) -> None:
        self.network_table.putNumber(
            "CANCoder Turn Rotations", self.cancoder.get_absolute_position().value
        )
        self.network_table.putNumber(
            "Turn Motor Rotations", self.turn_encoder.getPosition()
        )
        self.network_table.putNumber(
            "Turn Motor Angle", self.getPosition().angle.degrees()
        )
        self.network_table.putNumber(
            "Drive Rotations", self.drive_encoder.getPosition()
        )
        self.network_table.putNumber(
            "Drive Distance (ft)", self.getPosition().distance_ft
        )
        self.network_table.putNumber("Setpoint Angle (deg)", self.module_state.angle.degrees())
        self.network_table.putNumber("Setpoint Speed (fps)", self.module_state.speed_fps)
        if (
            self.network_table.getNumber("Drive P", self.drive_pid.getP())
            != self.drive_pid.getP()
        ):
            self.drive_pid.setP(self.network_table.getNumber("Drive P", 6e-5))

        if (
            self.network_table.getNumber("Drive I", self.drive_pid.getI())
            != self.drive_pid.getI()
        ):
            self.drive_pid.setI(self.network_table.getNumber("Drive I", 6e-5))

        if (
            self.network_table.getNumber("Drive D", self.drive_pid.getD())
            != self.drive_pid.getD()
        ):
            self.drive_pid.setD(self.network_table.getNumber("Drive D", 6e-5))

        if (
            self.network_table.getNumber("Turn P", self.turn_pid.getP())
            != self.turn_pid.getP()
        ):
            self.turn_pid.setP(self.network_table.getNumber("Turn P", 6e-5))

        if (
            self.network_table.getNumber("Turn I", self.turn_pid.getI())
            != self.turn_pid.getI()
        ):
            self.turn_pid.setI(self.network_table.getNumber("Turn I", 6e-5))

        if (
            self.network_table.getNumber("Turn D", self.turn_pid.getD())
            != self.turn_pid.getD()
        ):
            self.turn_pid.setD(self.network_table.getNumber("Turn D", 6e-5), 0)

    def setDesiredState(self, desiredState: SwerveModuleState):
        currAnglePos = self.turn_encoder.getPosition()
        currAngleRotation = Rotation2d(0).fromDegrees(currAnglePos)
        optimalState: SwerveModuleState = SwerveModuleState.optimize(
            desiredState, currAngleRotation
        )
        self.module_state = optimalState

        velocity = optimalState.speed
        self.drive_pid.setReference(velocity, CANSparkLowLevel.ControlType.kVelocity)
        self.turn_pid.setReference(inputModulus(optimalState.angle.degrees(), 0, 360) / 360, CANSparkLowLevel.ControlType.kPosition)

    def getModulePosition(self) -> Translation2d:
        is_front = self.name[0] == "f"
        is_left = self.name[1] == "l"
        return Translation2d(
            inchesToMeters(10.5) * (1 if is_front else -1),
            inchesToMeters(10.5) * (1 if is_left else -1),
        )

    def getPosition(self) -> SwerveModulePosition:
        # drive rotations
        dPosition = self.drive_encoder.getPosition()
        # rotations * 2pi * radius
        dMeters = dPosition * 2 * math.pi * inchesToMeters(2.0)

        thetaPosition = Rotation2d(0).fromDegrees(self.turn_encoder.getPosition())

        return SwerveModulePosition(distance=dMeters, angle=thetaPosition)

    def set_drive_idle(self, coast: bool):
        self.drive_motor.setIdleMode(
            CANSparkMax.IdleMode.kCoast if coast else CANSparkMax.IdleMode.kBrake
        )

    def set_turn_idle(self, coast: bool):
        self.turn_motor.setIdleMode(
            CANSparkMax.IdleMode.kCoast if coast else CANSparkMax.IdleMode.kBrake
        )
