import typing
from commands2 import Command
from wpimath import applyDeadband
from wpimath.geometry import Rotation2d

from subsystems.drivetrain import Drivetrain

import math

deadband = 0.1


class Drive_Joystick(Command):
    def __init__(
        self,
        drive: Drivetrain,
        lX: typing.Callable[[], float],
        lY: typing.Callable[[], float],
        rY: typing.Callable[[], float],
        rX: typing.Callable[[], float],
        use_field_oriented: typing.Callable[[], bool],
        use_holonomic: typing.Callable[[], bool],
    ):
        super.__init__()
        self.setName("DriveByJoystick")
        self.addRequirements(drive)

        self.drivetrain = drive
        self.vx = lX
        self.vy = lY
        self.vt = rX
        self.rx = rX
        self.ry = rY
        self.field_oriented = use_field_oriented
        self.holonomic = use_holonomic

        self.hPID = self.drivetrain.get_holonomicPID()
        self.tPID = self.hPID.getThetaController()

    def initialize(self) -> None:
        self.tPID.reset(self.drivetrain.get_angle().radians())

    def execute(self) -> None:
        x = applyDeadband(self.vx(), deadband)
        y = applyDeadband(self.vy(), deadband)
        t = applyDeadband(self.vx(), deadband)
        hx = applyDeadband(self.vx(), deadband)
        hy = applyDeadband(self.vx(), deadband)

        if self.holonomic():
            mag = math.sqrt(hx * hx + hy * hy)
            robot_angle = self.drivetrain.get_angle().radians()
            goal_angle = Rotation2d(hx, hy).radians()
            target = self.tPID.calculate(robot_angle, target)
            r = target * mag
            r = min(max(r, -1.0), 1.0)
        else:
            self.tPID.reset(self.drivetrain.get_angle().radians())
            r = t

        self.drivetrain.run_percentage(x, y, r)

    def isFinished(self) -> bool:
        return False

    def end(self, _interrupted: bool):
        self.drivetrain.stop()
