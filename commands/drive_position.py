from commands2 import Command
from wpimath.controller import PIDController
from wpimath.geometry import Pose2d, Rotation2d
from wpimath.units import inchesToMeters
from subsystems.drivetrain import Drivetrain


class Drive_Position(Command):
    def __init__(self, drivetrain: Drivetrain, desired_position: Pose2d):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)
        self.desired = desired_position

        self.x_pid = PIDController(6e-5, 0, 0)
        self.y_pid = PIDController(6e-5, 0, 0)
        self.t_pid = PIDController(6e-5, 0, 0)

        self.t_pid.enableContinuousInput(-180, 180)

        self.x_pid.setTolerance(inchesToMeters(3))
        self.y_pid.setTolerance(inchesToMeters(3))
        self.t_pid.setTolerance(7.5)

    def initialize(self):
        self.x_pid.reset()
        self.y_pid.reset()
        self.t_pid.reset()

    def execute(self):
        position = self.drivetrain.odometry.getEstimatedPosition()
        x_out = self.x_pid.calculate(position.X(), self.desired.X())
        y_out = self.y_pid.calculate(position.Y(), self.desired.Y())
        t_out = self.t_pid.calculate(
            position.rotation().degrees(), self.desired.rotation().degrees()
        )
        self.drivetrain.run_percentage(x_out, y_out, t_out)

    def isFinished(self) -> bool:
        return (
            self.x_pid.atSetpoint()
            and self.y_pid.atSetpoint()
            and self.t_pid.atSetpoint()
        )
