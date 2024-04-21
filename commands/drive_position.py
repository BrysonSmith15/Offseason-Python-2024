from commands2 import Command
from ntcore import NetworkTableInstance
from wpimath.geometry import Pose2d

from subsystems.drivetrain import Drivetrain


class Drive_Position(Command):
    def __init__(self, drivetrain: Drivetrain, desired_position: Pose2d):
        super().__init__()
        self.net_table = NetworkTableInstance.getDefault().getTable("Drivetrain")
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)
        self.desired = desired_position

        self.x_pid = self.drivetrain.x_pid
        self.y_pid = self.drivetrain.y_pid
        self.t_pid = self.drivetrain.t_pid

    def initialize(self):
        # position = self.drivetrain.odometry.getEstimatedPosition()
        # self.t_pid.reset(
        #     position.rotation().radians()
        # + self.drivetrain.t_pid.getPositionTolerance()
        # self.drivetrain.get_angle().radians()
        # )
        pass

    def execute(self):
        position = self.drivetrain.odometry.getEstimatedPosition()
        x_out = self.x_pid.calculate(position.X(), self.desired.X())
        y_out = self.y_pid.calculate(position.Y(), self.desired.Y())
        t_out = self.t_pid.calculate(
            measurement=-position.rotation().radians(),
            goal=self.desired.rotation().radians(),
        )
        self.drivetrain.__ntTbl__.putNumber("DrivePose/Desired X", self.desired.X())
        self.drivetrain.__ntTbl__.putNumber("DrivePose/Desired Y", self.desired.Y())
        self.drivetrain.__ntTbl__.putNumber(
            "DrivePose/Desired Degrees", self.desired.rotation().degrees()
        )
        self.drivetrain.__ntTbl__.putNumber("DrivePose/x_out", x_out)
        self.drivetrain.__ntTbl__.putNumber("DrivePose/y_out", y_out)
        self.drivetrain.__ntTbl__.putNumber("DrivePose/theta_out", t_out)

        self.drivetrain.run_percentage(x_out, y_out, t_out)

    def isFinished(self) -> bool:
        self.net_table.putBoolean("DrivePose/X At Setpoint", self.x_pid.atSetpoint())
        self.net_table.putBoolean("DrivePose/Y At Setpoint", self.y_pid.atSetpoint())
        self.net_table.putBoolean(
            "DrivePose/Theta At Setpoint", self.t_pid.atSetpoint()
        )
        self.net_table.putNumber("DrivePose/X Error", self.x_pid.getPositionError())
        self.net_table.putNumber("DrivePose/Y Error", self.y_pid.getPositionError())
        self.net_table.putNumber("DrivePose/Theta Error", self.t_pid.getPositionError())
        return (
            self.x_pid.atSetpoint()
            and self.y_pid.atSetpoint()
            and self.t_pid.atSetpoint()
        )

    def end(self, _interrupted: bool) -> None:
        self.x_pid.reset(self.drivetrain.get_pose().X())
        self.y_pid.reset(self.drivetrain.get_pose().Y())
        self.t_pid.reset(self.drivetrain.get_angle().radians())

    def __str__(self) -> str:
        return (
            f"Drive Position going to {self.desired} Scheduled?: {self.isScheduled()}"
        )
