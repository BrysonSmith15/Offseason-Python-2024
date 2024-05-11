from commands2 import Command
from wpimath.geometry import Rotation2d
from wpimath.kinematics import ChassisSpeeds

from subsystems.drivetrain import Drivetrain


class DriveAngle(Command):
    def __init__(self, drivetrain: Drivetrain, angle: Rotation2d):
        super().__init__()
        self.drivetrain = drivetrain
        self.angle = angle
        self.addRequirements(drivetrain)

    def execute(self) -> None:
        self.drivetrain.run_chassis_speeds(
            ChassisSpeeds(
                0,
                0,
                self.drivetrain.t_pid.calculate(
                    measurement=self.drivetrain.get_angle().radians(),
                    goal=self.angle.radians(),
                ),
            ),
        )

    def isFinished(self) -> bool:
        return self.drivetrain.t_pid.atSetpoint()

    def end(self, interrupted: bool) -> None:
        self.drivetrain.stop()
