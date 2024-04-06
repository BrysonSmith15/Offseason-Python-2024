from commands2 import Command
from wpimath.controller import PIDController
from wpimath.geometry import Pose2d, Rotation2d
from wpimath.units import inchesToMeters
from subsystems.drivetrain import Drivetrain
from utils.NT_Tunable_Float import NTTunableFloat


class Drive_Position(Command):
    def __init__(self, drivetrain: Drivetrain, desired_position: Pose2d):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)
        self.desired = desired_position

        self.xp_tuner = NTTunableFloat(
            "Positional Drive X P Value", 6e-5, persistent=True
        )
        self.xi_tuner = NTTunableFloat("Positional Drive X I Value", 0, persistent=True)
        self.xd_tuner = NTTunableFloat("Positional Drive X D Value", 0, persistent=True)

        self.yp_tuner = NTTunableFloat(
            "Positional Drive Y P Value", 6e-5, persistent=True
        )
        self.yi_tuner = NTTunableFloat("Positional Drive Y I Value", 0, persistent=True)
        self.yd_tuner = NTTunableFloat("Positional Drive Y D Value", 0, persistent=True)

        self.tp_tuner = NTTunableFloat(
            "Positional Drive Rotation P Value", 6e-5, persistent=True
        )
        self.ti_tuner = NTTunableFloat(
            "Positional Drive Rotation I Value", 0, persistent=True
        )
        self.td_tuner = NTTunableFloat(
            "Positional Drive Rotation D Value", 0, persistent=True
        )

        self.x_pid = PIDController(
            self.xp_tuner.get(), self.xi_tuner.get(), self.xd_tuner.get()
        )
        self.y_pid = PIDController(
            self.yp_tuner.get(), self.yi_tuner.get(), self.yd_tuner.get()
        )
        self.t_pid = PIDController(
            self.tp_tuner.get(), self.ti_tuner.get(), self.td_tuner.get()
        )

        self.t_pid.enableContinuousInput(-180, 180)

        self.x_pid.setTolerance(inchesToMeters(3))
        self.y_pid.setTolerance(inchesToMeters(3))
        self.t_pid.setTolerance(7.5)

    def initialize(self):
        self.x_pid.reset()
        self.y_pid.reset()
        self.t_pid.reset()

        # reset values in an easy way
        self.x_pid = PIDController(
            self.xp_tuner.get(), self.xi_tuner.get(), self.xd_tuner.get()
        )
        self.y_pid = PIDController(
            self.yp_tuner.get(), self.yi_tuner.get(), self.yd_tuner.get()
        )
        self.t_pid = PIDController(
            self.tp_tuner.get(), self.ti_tuner.get(), self.td_tuner.get()
        )

    def execute(self):
        position = self.drivetrain.odometry.getEstimatedPosition()
        x_out = self.x_pid.calculate(position.X(), self.desired.X())
        y_out = self.y_pid.calculate(position.Y(), self.desired.Y())
        t_out = self.t_pid.calculate(
            position.rotation().degrees(), self.desired.rotation().degrees()
        )
        self.drivetrain.run_percentage(x_out, y_out, t_out)

    def isFinished(self) -> bool:
        return (
            self.x_pid.atSetpoint()
            and self.y_pid.atSetpoint()
            and self.t_pid.atSetpoint()
        )
