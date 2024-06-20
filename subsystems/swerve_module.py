import math

from commands2 import Subsystem
from ntcore import NetworkTable, NetworkTableInstance
from phoenix6.hardware import CANcoder
from rev import CANSparkLowLevel, CANSparkMax, SparkRelativeEncoder
from wpimath import inputModulus
from wpimath.controller import PIDController
from wpimath.filter import SlewRateLimiter
from wpimath.geometry import Rotation2d, Translation2d
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState
from wpimath.units import inchesToMeters, feetToMeters

# consts
drive_P = 1e-3
drive_I = 0.0
drive_D = 1e-4


turn_P = 0.006
turn_I = 0.0
turn_D = 1e-6


class SwerveModule(Subsystem):
    drive_motor: CANSparkMax = None
    turn_motor: CANSparkMax = None
    cancoder: CANcoder = None
    drive_encoder: SparkRelativeEncoder = None
    turn_encoder: SparkRelativeEncoder = None
    module_position: Translation2d = None
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
        self.pid_net_table = NetworkTableInstance.getDefault().getTable(
            "Swervemodule/Swerve PID"
        )

        self.cancoder = CANcoder(encoder_id)
        self.turn_motor = CANSparkMax(
            turn_id, CANSparkLowLevel.MotorType.kBrushless)
        self.drive_motor = CANSparkMax(
            drive_id, CANSparkLowLevel.MotorType.kBrushless)

        self.cancoder.set_position(self.cancoder.get_absolute_position().value)

        self.turn_motor.setInverted(turn_inverted)

        self.turn_pid = PIDController(turn_P, turn_I, turn_D)
        # self.turn_pid.setP(turn_P)
        # self.turn_pid.setI(turn_I)
        # self.turn_pid.setD(turn_D)
        self.turn_pid.enableContinuousInput(-180, 180)

        self.drive_encoder = self.drive_motor.getEncoder()
        self.drive_encoder.setPosition(0)
        self.drive_encoder.setPositionConversionFactor(1 / 8.14)
        self.drive_encoder.setVelocityConversionFactor(1 / 8.14)

        self.drive_pid = PIDController(drive_P, drive_I, drive_D)
        # self.drive_pid.setP(drive_P)
        # self.drive_pid.setI(drive_I)
        # self.drive_pid.setD(drive_D)
        # accelerate fully in 1 second, decelerate in 10
        self.drive_limiter = SlewRateLimiter(2, -100)

        self.setName(f"SwerveModule/{subsystem_name}")

        self.pid_net_table.putNumber("Turn P", self.turn_pid.getP())
        self.pid_net_table.putNumber("Turn I", self.turn_pid.getI())
        self.pid_net_table.putNumber("Turn D", self.turn_pid.getD())
        self.pid_net_table.putNumber("Drive P", self.turn_pid.getP())
        self.pid_net_table.putNumber("Drive I", self.turn_pid.getI())
        self.pid_net_table.putNumber("Drive D", self.turn_pid.getD())

        self.drive_velocity = 0

        self.drive_motor.setPeriodicFramePeriod(
            CANSparkLowLevel.PeriodicFrame.kStatus3, 50
        )
        self.turn_motor.setPeriodicFramePeriod(
            CANSparkLowLevel.PeriodicFrame.kStatus3, 50
        )
        self.drive_motor.setPeriodicFramePeriod(
            CANSparkLowLevel.PeriodicFrame.kStatus4, 50
        )
        self.turn_motor.setPeriodicFramePeriod(
            CANSparkLowLevel.PeriodicFrame.kStatus4, 50
        )
        self.drive_motor.setPeriodicFramePeriod(
            CANSparkLowLevel.PeriodicFrame.kStatus5, 50
        )
        self.turn_motor.setPeriodicFramePeriod(
            CANSparkLowLevel.PeriodicFrame.kStatus5, 50
        )
        self.drive_motor.setPeriodicFramePeriod(
            CANSparkLowLevel.PeriodicFrame.kStatus6, 50
        )
        self.turn_motor.setPeriodicFramePeriod(
            CANSparkLowLevel.PeriodicFrame.kStatus6, 50
        )
        self.drive_motor.setCANTimeout(50)
        self.turn_motor.setCANTimeout(50)

        self.optimal_state = SwerveModuleState(0, Rotation2d(0))

    def periodic(self) -> None:
        self.network_table.putNumber(
            "CANCoder Turn Rotations", self.cancoder.get_absolute_position().value
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
        self.network_table.putNumber(
            "Setpoint Angle (deg)", self.optimal_state.angle.degrees()
        )
        self.network_table.putNumber(
            "Setpoint Speed (fps)", self.optimal_state.speed_fps
        )
        self.drive_velocity = self.drive_encoder.getVelocity()
        * -2
        * math.pi
        # 1 / 6 -> 2 in radius--1/6 becuase otherwise it is in/s, not fps
        * (1 / 6)
        self.network_table.putNumber(
            "Drive Speed (fps)",
            self.drive_velocity,
        )
        if (
            self.pid_net_table.getNumber("Turn P", self.turn_pid.getP())
            != self.turn_pid.getP()
        ):
            self.turn_pid.setP(self.pid_net_table.getNumber("Turn P", 6e-5))

        if (
            self.pid_net_table.getNumber("Turn I", self.turn_pid.getI())
            != self.turn_pid.getI()
        ):
            self.turn_pid.setI(self.pid_net_table.getNumber("Turn I", 6e-5))

        if (
            self.pid_net_table.getNumber("Turn D", self.turn_pid.getD())
            != self.turn_pid.getD()
        ):
            self.turn_pid.setD(self.pid_net_table.getNumber("Turn D", 6e-5))

        if (
            self.pid_net_table.getNumber("Drive P", self.drive_pid.getP())
            != self.drive_pid.getP()
        ):
            self.drive_pid.setP(self.pid_net_table.getNumber("Drive P", 6e-5))

        if (
            self.pid_net_table.getNumber("Drive I", self.drive_pid.getI())
            != self.drive_pid.getI()
        ):
            self.drive_pid.setI(self.pid_net_table.getNumber("Drive I", 0))

        if (
            self.pid_net_table.getNumber("Drive D", self.drive_pid.getD())
            != self.drive_pid.getD()
        ):
            self.drive_pid.setD(self.pid_net_table.getNumber("Drive D", 6e-5))

    def setDesiredState(self, desiredState: SwerveModuleState, max_velocity_mps: float):
        # currAnglePos = self.turn_encoder.getPosition()
        currAnglePos = self.getPosition().angle.degrees()
        currAngleRotation = Rotation2d().fromDegrees(currAnglePos)
        optimalState: SwerveModuleState = SwerveModuleState.optimize(
            desiredState, currAngleRotation
        )
        self.optimal_state = optimalState

        velocity = optimalState.speed
        # self.drive_pid.setReference(velocity, CANSparkLowLevel.ControlType.kVelocity)
        # drive_out = self.drive_pid.calculate(
        #     velocity,
        #     self.drive_encoder.getVelocity() * -2 * math.pi * inchesToMeters(2.0),
        # )
        drive_out = self.drive_limiter.calculate(velocity / max_velocity_mps)
        drive_out = 1 if drive_out > 1 else -1 if drive_out < -1 else drive_out
        self.network_table.putNumber("Drive Out", drive_out)
        self.drive_motor.set(drive_out)
        # self.drive_motor.set(self.drive_limiter.calculate(velocity / 15))
        turn_out = self.turn_pid.calculate(
            self.getPosition().angle.degrees(),
            inputModulus(optimalState.angle.degrees(), -180, 180),
        )
        turn_out = 1 if turn_out > 1 else -1 if turn_out < -1 else turn_out
        self.turn_motor.set(turn_out)
        # self.turn_pid.setReference(
        #     inputModulus(optimalState.angle.degrees(), -180, 180) / 180,
        #     CANSparkLowLevel.ControlType.kPosition,
        # )

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

        thetaPosition = self.get_turn_angle()

        return SwerveModulePosition(distance=dMeters, angle=thetaPosition)

    def get_turn_angle(self) -> Rotation2d:
        return Rotation2d().fromDegrees(
            self.cancoder.get_absolute_position().value
            * 360
            # -inputModulus(self.turn_encoder.getPosition() * 360, -180, 180)
        )

    def get_state(self) -> SwerveModuleState:
        SwerveModuleState(feetToMeters(self.drive_velocity),
                          self.get_turn_angle())

    def set_drive_idle(self, coast: bool):
        self.drive_motor.setIdleMode(
            CANSparkMax.IdleMode.kCoast if coast else CANSparkMax.IdleMode.kBrake
        )

    def set_turn_idle(self, coast: bool):
        self.turn_motor.setIdleMode(
            CANSparkMax.IdleMode.kCoast if coast else CANSparkMax.IdleMode.kBrake
        )
