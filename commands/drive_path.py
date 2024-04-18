from typing import Tuple

from commands2 import Command
from wpimath.geometry import Pose2d

from subsystems.drivetrain import Drivetrain


class drive_path(Command):
    def __init__(self, drivetrain: Drivetrain, points: [Pose2d]):
        super().__init__()
        self.addRequirements(drivetrain)

        self.drivetrain = drivetrain
        self.points = points
        self.path = self.curve(points[0], points[1], points[2], 10)
        self.x_pid = self.drivetrain.x_pid
        self.y_pid = self.drivetrain.y_pid
        self.t_pid = self.drivetrain.t_pid

    def initialize(self) -> None:
        self.path = self.curve(self.points[0], self.points[1], self.points[2], 10)
        # set coast
        self.drivetrain.set_drive_idle(True)

    def execute(self) -> None:
        pass

    def isFinished(self) -> bool:
        return True

    def end(self, interrupted: bool) -> None:
        # set brake
        self.drivetrain.set_drive_idle(False)
        self.drivetrain.stop()

    @staticmethod
    def curve(
        p0: Tuple[float, float],
        p1: Tuple[float, float],
        p2: Tuple[float, float],
        nTimes: int = 1000,
    ):
        """
        given the three control points
        generate a curve that gets "kinda close" to each with midpoints 'n stuff

        My docs are the best ever, I promise
        """

        def lerp(v0: float, v1: float, t: float):
            return (1 - t) * v0 + t * v1

        p01_interpolation = list(
            zip(
                [lerp(p0[0], p1[0], i / nTimes) for i in range(1, nTimes + 1)],
                [lerp(p0[1], p1[1], i / nTimes) for i in range(1, nTimes + 1)],
            )
        )
        p12_interpolation = list(
            zip(
                [lerp(p1[0], p2[0], i / nTimes) for i in range(1, nTimes + 1)],
                [lerp(p1[1], p2[1], i / nTimes) for i in range(1, nTimes + 1)],
            )
        )
        return list(
            zip(
                [
                    lerp(p01_interpolation[i][0], p12_interpolation[i][0], i / nTimes)
                    for i in range(nTimes)
                ],
                [
                    lerp(p01_interpolation[i][1], p12_interpolation[i][1], i / nTimes)
                    for i in range(nTimes)
                ],
            )
        )
