import commands2
from commands2 import SequentialCommandGroup, WaitCommand
from wpimath.geometry import Pose2d

from commands.drive_position import Drive_Position
from commands.elevator_top import Elevator_Top
from commands.intake_run import Intake_Run
from commands.shoot import Shoot
from subsystems.drivetrain import Drivetrain
from subsystems.elevator import Elevator
from subsystems.intake import Intake
from subsystems.shooter import Shooter


# TODO: Make it really good, like this one: https://www.youtube.com/watch?v=dompT_VuHxs


def Shoot_Only(
    elevator: Elevator,
    intake: Intake,
    shooter: Shooter,
) -> SequentialCommandGroup:
    """
    shoot a note
    """
    return (
        Elevator_Top(elevator)
        .withTimeout(2)
        .andThen(Intake_Run(intake, -0.25))
        .withTimeout(1)
        .andThen(
            Shoot(shooter).alongWith(WaitCommand(2).andThen(Intake_Run(intake, 1.0)))
        )
    )


def Shoot_And_Drive(
    drivetrain: Drivetrain,
    elevator: Elevator,
    intake: Intake,
    shooter: Shooter,
    starting_pose: Pose2d,
) -> SequentialCommandGroup:
    """
    Shoot a note then cross the auto line
    """
    new_pose = Pose2d(
        starting_pose.X() + 0.5, starting_pose.Y(), starting_pose.rotation()
    )
    return Shoot_Only(elevator, intake, shooter).andThen(
        Drive_Position(drivetrain, new_pose)
    )


def Nothing():
    """
    Do Nothing in auto
    """
    return commands2.cmd.none()
