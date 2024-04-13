from commands2 import Command
from ntcore import NetworkTableInstance
from wpimath.geometry import Pose2d

from subsystems.drivetrain import Drivetrain


class Drive_Position(Command):
    def __init__(self, drivetrain: Drivetrain, desired_position: Pose2d):
        super().__init__()
        self.net_table = NetworkTableInstance.getDefault().getTable("Drive_Position")
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)
        self.desired = desired_position

        self.x_pid = self.drivetrain.x_pid
        self.y_pid = self.drivetrain.y_pid
        self.t_pid = self.drivetrain.t_pid

    def initialize(self):
        self.x_pid.setPID(
            self.net_table.getNumber("x_kp", self.x_pid.getP()),
            self.net_table.getNumber("x_ki", self.x_pid.getI()),
            self.net_table.getNumber("x_kd", self.x_pid.getD()),
        )
        self.y_pid.setPID(
            self.net_table.getNumber("y_kp", self.y_pid.getP()),
            self.net_table.getNumber("y_ki", self.y_pid.getI()),
            self.net_table.getNumber("y_kd", self.y_pid.getD()),
        )
        self.x_pid.setPID(
            self.net_table.getNumber("theta_kp", self.t_pid.getP()),
            self.net_table.getNumber("theta_ki", self.t_pid.getI()),
            self.net_table.getNumber("theta_kd", self.t_pid.getD()),
        )
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
