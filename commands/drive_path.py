from commands2 import Command
from ntcore import NetworkTableInstance
from wpimath.geometry import Pose2d, Rotation2d

from subsystems.drivetrain import Drivetrain


class Drive_Path(Command):
    def __init__(self, drivetrain: Drivetrain, points: [Pose2d]):
        super().__init__()
        self.addRequirements(drivetrain)

        self.drivetrain = drivetrain
        self.points = points

        self.path = []  # self.curve(points[0], points[1], points[2], 5)
        self.x_pid = self.drivetrain.x_pid
        self.y_pid = self.drivetrain.y_pid
        self.t_pid = self.drivetrain.t_pid
        self.net_table = NetworkTableInstance.getDefault().getTable(
            "Drive Path"
        )

        self.counter = 0

    def initialize(self) -> None:
        curr_position = self.drivetrain.get_pose()
        self.x_pid.reset(curr_position.X())
        self.y_pid.reset(curr_position.Y())
        self.t_pid.reset(curr_position.rotation().radians())
        self.path = self.curve(
            self.points[0], self.points[1], self.points[2], 4
        )
        print(self.path)
        # set coast
        self.drivetrain.set_drive_idle(True)
        self.counter = 0

    def execute(self) -> None:
        position = self.drivetrain.get_pose()
        x_out = self.x_pid.calculate(
            measurement=position.X(), goal=self.path[0].X()
        )
        y_out = self.y_pid.calculate(
            measurement=position.Y(), goal=self.path[0].Y()
        )
        t_out = self.t_pid.calculate(
            measurement=-position.rotation().radians(),
            goal=self.path[0].rotation().radians(),
        )
        self.net_table.putNumber("Goals/X (ft)", self.path[0].x_feet)
        self.net_table.putNumber("Goals/Y (ft)", self.path[0].y_feet)
        self.net_table.putNumber(
            "Goals/Theta (degrees)", self.path[0].rotation().degrees()
        )
        self.drivetrain.run_percentage(-x_out, -y_out, t_out)

    def isFinished(self) -> bool:
        position = self.drivetrain.get_pose()
        self.x_pid.calculate(measurement=position.X(), goal=self.path[0].X())
        self.y_pid.calculate(measurement=position.Y(), goal=self.path[0].Y())
        self.t_pid.calculate(
            measurement=-position.rotation().radians(),
            goal=self.path[0].rotation().radians(),
        )
        if (
            self.x_pid.atSetpoint()
            and self.y_pid.atSetpoint()
            and self.t_pid.atSetpoint()
        ):
            self.counter += 1
        else:
            self.counter = 0
        if self.counter >= 5:
            self.path.pop(0)
        print(self.path, end="\n\n")
        return len(self.path) == 0

    def end(self, interrupted: bool) -> None:
        # set brake
        self.drivetrain.set_drive_idle(False)
        self.drivetrain.stop()

    @staticmethod
    def curve(
        p0: Pose2d,
        p1: Pose2d,
        p2: Pose2d,
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
                [
                    lerp(p0.X(), p1.X(), i / nTimes)
                    for i in range(1, nTimes + 1)
                ],
                [
                    lerp(p0.Y(), p1.Y(), i / nTimes)
                    for i in range(1, nTimes + 1)
                ],
            )
        )
        p12_interpolation = list(
            zip(
                [
                    lerp(p1.X(), p2.X(), i / nTimes)
                    for i in range(1, nTimes + 1)
                ],
                [
                    lerp(p1.Y(), p2.Y(), i / nTimes)
                    for i in range(1, nTimes + 1)
                ],
            )
        )
        a = list(
            zip(
                [
                    lerp(
                        p01_interpolation[i][0],
                        p12_interpolation[i][0],
                        i / nTimes,
                    )
                    for i in range(nTimes)
                ],
                [
                    lerp(
                        p01_interpolation[i][1],
                        p12_interpolation[i][1],
                        i / nTimes,
                    )
                    for i in range(nTimes)
                ],
            )
        )
        return [
            Pose2d(
                b[0],
                b[1],
                Rotation2d.fromDegrees(
                    lerp(
                        p0.rotation().degrees(),
                        p2.rotation().degrees(),
                        idx / (len(a) - 1),
                    )
                ),
            )
            for idx, b in enumerate(a)
        ]
