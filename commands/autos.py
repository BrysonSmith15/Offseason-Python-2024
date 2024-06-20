import commands2
from commands2 import SequentialCommandGroup, WaitCommand
from wpimath.geometry import Pose2d, Rotation2d
from wpimath.units import feetToMeters

from commands.drive_path import Drive_Path
from commands.elevator_top import Elevator_Top
from commands.intake_run import Intake_Run
from commands.shoot import Shoot
from subsystems.drivetrain import Drivetrain
from subsystems.elevator import Elevator
from subsystems.intake import Intake
from subsystems.shooter import Shooter


# TODO: Make it really good, like this one: https://www.youtube.com/watch?v=dompT_VuHxs


def _red_pose_convert(pose: Pose2d):
    x = pose.X()
    y = pose.Y()
    t = pose.rotation()
    return Pose2d(
        feetToMeters(54) - x, feetToMeters(27) -
        y, Rotation2d.fromDegrees(180) - t
    )


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
            (
                Shoot(shooter).alongWith(
                    WaitCommand(2).andThen(Intake_Run(intake, 1.0))
                )
            ).withTimeout(5)
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
    drivetrain.odometry.resetPosition(
        drivetrain.get_angle(), drivetrain.get_module_positions(), starting_pose
    )
    return Shoot_Only(elevator, intake, shooter).andThen(
        Drive_Path(drivetrain, [new_pose, new_pose, new_pose])
    )


def Drive_Around(drivetrain: Drivetrain, red: bool = False) -> SequentialCommandGroup:
    p0 = Pose2d(1.4, 3.5, Rotation2d.fromDegrees(180))
    p1 = Pose2d(0, 0, Rotation2d(0))
    p2 = Pose2d(feetToMeters(54) / 2 + 1.75, 0.8, Rotation2d.fromDegrees(0))
    if red:
        p0 = _red_pose_convert(p0)
        p1 = _red_pose_convert(p1)
        p2 = _red_pose_convert(p2)
    return SequentialCommandGroup(
        Drive_Path(
            drivetrain,
            [p0, p1, p2],
        ),
        Drive_Path(
            drivetrain,
            [p2, p1, p0],
        ),
    )


def Nothing():
    """
    Do Nothing in auto
    """
    return commands2.cmd.none()
