import math
import typing

from commands2 import Command
from ntcore import NetworkTableInstance
from wpimath import applyDeadband
from wpimath.geometry import Rotation2d
from wpimath.kinematics import ChassisSpeeds
from wpimath.units import meters_per_second, radians_per_second

from subsystems.drivetrain import Drivetrain

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
        super().__init__()
        self.setName("DriveByJoystick")
        self.addRequirements(drive)
        self.network_table = NetworkTableInstance.getDefault().getTable("Drivetrain")

        self.drivetrain = drive
        self.vx = lX
        self.vy = lY
        self.vt = rX
        self.rx = rX
        self.ry = rY
        self.field_oriented = use_field_oriented
        self.holonomic = use_holonomic

        self.xPID = self.drivetrain.x_pid
        self.yPID = self.drivetrain.y_pid
        self.tPID = self.drivetrain.t_pid

    def initialize(self) -> None:
        self.tPID.reset(
            measuredPosition=self.drivetrain.get_pose().rotation().radians()
        )

    def execute(self) -> None:
        x = applyDeadband(self.vx(), deadband)
        y = applyDeadband(self.vy(), deadband)
        t = applyDeadband(self.vt(), deadband)
        hx = applyDeadband(self.rx(), deadband)
        hy = applyDeadband(self.ry(), deadband)

        if self.holonomic():
            # TODO: Make good
            mag = math.sqrt(hx * hx + hy * hy)
            robot_angle = self.drivetrain.get_angle().radians()
            goal_angle = Rotation2d(-hy, -hx).radians()
            self.network_table.putNumber("DriveJoystick/Goal Angle", goal_angle)
            target = self.tPID.calculate(robot_angle, goal_angle)
            self.network_table.putNumber("DriveJoystick/target", target)
            r = target * mag
            r = min(max(r, -1.0), 1.0)
        else:
            # r = self.drivetrain.t_limiter.calculate(t)
            r = t

        if self.field_oriented():
            speeds = ChassisSpeeds.fromFieldRelativeSpeeds(
                x * self.drivetrain.maxVelocity,
                y * self.drivetrain.maxVelocity,
                r * self.drivetrain.maxAngularVelocity,
                self.drivetrain.get_angle(),
            )
        else:
            # not field oriented is not good?
            # in the simulator it just does the same thing
            speeds = ChassisSpeeds(
                meters_per_second(x * self.drivetrain.maxVelocity),
                meters_per_second(y * self.drivetrain.maxVelocity),
                radians_per_second(r * self.drivetrain.maxAngularVelocity),
            )
        self.network_table.putBoolean(
            "DriveJoystick/FieldOriented", self.field_oriented()
        )
        # self.drivetrain.run_chassis_speeds(speeds)
        self.drivetrain.run_percentage(x, y, r)
        self.network_table.putNumber("DriveJoystick/X%", x)
        self.network_table.putNumber("DriveJoystick/Y%", y)
        self.network_table.putNumber("DriveJoystick/Theta%", r)

    def isFinished(self) -> bool:
        return False

    def end(self, _interrupted: bool):
        self.drivetrain.stop()
