from commands2 import Command
from wpimath.geometry import Pose2d
from wpimath.kinematics import ChassisSpeeds

from subsystems.drivetrain import Drivetrain


class DriveTranslation(Command):
    def __init__(self, drivetrain: Drivetrain, offset: Pose2d):
        super().__init__()
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

    def execute(self) -> None:
        curr = self.drivetrain.get_pose()
        x_out = self.drivetrain.x_pid.calculate(
            measurement=curr.x, goal=self.new_pose.x
        )
        y_out = self.drivetrain.x_pid.calculate(
            measurement=curr.y, goal=self.new_pose.y
        )
        t_out = self.drivetrain.x_pid.calculate(
            measurement=curr.rotation().radians(),
            goal=self.new_pose.rotation().radians(),
        )
        self.drivetrain.run_chassis_speeds(ChassisSpeeds(x_out, y_out, t_out))

    def isFinished(self) -> bool:
        return True

    def end(self, interrupted: bool) -> None:
        pass
