from commands2 import Command
from ntcore import NetworkTableInstance
from wpimath.geometry import Pose2d
from wpimath.kinematics import ChassisSpeeds

from subsystems.drivetrain import Drivetrain


class DriveTranslation(Command):
    def __init__(self, drivetrain: Drivetrain, offset: Pose2d):
        super().__init__()
        self.net_table = NetworkTableInstance.getDefault().getTable("DriveTranslation")
        self.drivetrain = drivetrain
        self.offset = offset
        self.addRequirements(drivetrain)
        curr = self.drivetrain.get_pose()
        self.new_pose = Pose2d(
            curr.x + self.offset.x,
            curr.y + self.offset.y,
            curr.rotation() + self.offset.rotation(),
        )

    def initialize(self):
        curr = self.drivetrain.get_pose()
        self.new_pose = Pose2d(
            curr.x + self.offset.x,
            curr.y + self.offset.y,
            curr.rotation() + self.offset.rotation(),
        )
        self.net_table.putNumber("New X", self.new_pose.x)
        self.net_table.putNumber("New Y", self.new_pose.y)
        self.net_table.putNumber(
            "New Rotation (deg)", self.new_pose.rotation().degrees()
        )

    def execute(self) -> None:
        curr = self.drivetrain.get_pose()
        x_out = self.drivetrain.x_pid.calculate(
            measurement=-curr.x, goal=self.new_pose.x
        )
        y_out = self.drivetrain.x_pid.calculate(
            measurement=-curr.y, goal=self.new_pose.y
        )
        t_out = self.drivetrain.x_pid.calculate(
            measurement=-curr.rotation().radians(),
            goal=self.new_pose.rotation().radians(),
        )
        self.net_table.putNumber("X Out", x_out)
        self.net_table.putNumber("Y Out", y_out)
        self.net_table.putNumber("Rotational Out", t_out)

        self.drivetrain.run_chassis_speeds(ChassisSpeeds(x_out, y_out, t_out))

    def isFinished(self) -> bool:
        return (
            self.drivetrain.x_pid.atSetpoint()
            and self.drivetrain.y_pid.atSetpoint()
            and self.drivetrain.t_pid.atSetpoint()
        )

    def end(self, interrupted: bool) -> None:
        pass
