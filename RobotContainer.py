from wpilib import SendableChooser, SmartDashboard, Joystick
from commands2 import button  # , command
from wpimath.units import feetToMeters

# import commands2.cmd

from commands.drive_joystick import Drive_Joystick

from subsystems.drivetrain import Drivetrain
from subsystems.interface import Interface


class RobotContainer:
    def __init__(self) -> None:
        self.interface = Interface()
        self.drivetrain = Drivetrain()

    def set_default_commands(self) -> None:
        self.drivetrain.setDefaultCommand(
            Drive_Joystick(
                self.drivetrain,
                self.interface.get_drive_forward,
                self.interface.get_drive_side,
                self.interface.get_drive_holonomic_forward,
                self.interface.get_drive_turn,
                self.interface.get_drive_field_oriented,
                self.interface.get_drive_holonomic,
            )
        )

    def configure_bindings(self) -> None:
        self.interface.get_drive_defense_mode().onTrue(
            self.drivetrain.set_max_speed_command(feetToMeters(100.0))
        ).onFalse(self.drivetrain.set_max_speed_command(feetToMeters(15.0)))

        self.interface.get_drive_reset_gyro().onTrue(
            self.drivetrain.reset_gyro_command()
        )
