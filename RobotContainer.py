from wpilib import DriverStation, SendableChooser, SmartDashboard, Joystick
from commands2.button import Trigger
from wpimath.units import feetToMeters

# import commands2.cmd

from commands.drive_joystick import Drive_Joystick
from commands.elevator_bottom import Elevator_Bottom
from commands.elevator_top import Elevator_Top
from commands.intake_run import Intake_Run
from commands.led_chase import LED_Chase
from commands.shoot import Shoot

from subsystems.drivetrain import Drivetrain
from subsystems.interface import Interface
from subsystems.elevator import Elevator
from subsystems.leds import LEDs
from subsystems.shooter import Shooter
from subsystems.vision import Vision


class RobotContainer:
    def __init__(self) -> None:
        self.interface = Interface()
        self.drivetrain = Drivetrain()
        self.elevator = Elevator()
        self.shooter = Shooter()
        self.vision = Vision(self.drivetrain.get_odometry)
        self.leds = LEDs(9, 80)

        self.configure_bindings()

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
        # go really fast to fight and play defense
        self.interface.get_drive_defense_mode().onTrue(
            self.drivetrain.set_max_speed_command(feetToMeters(100.0))
        ).onFalse(self.drivetrain.set_max_speed_command(feetToMeters(15.0)))
        # reset the gyro on button press
        self.interface.get_drive_reset_gyro().onTrue(
            self.drivetrain.reset_gyro_command()
        )

        # move shooter to the top
        self.interface.get_elevator_up().onTrue(Elevator_Top(self.elevator))
        # move shooter to the bottom
        self.interface.get_elevator_down().onTrue(Elevator_Bottom(self.elevator))

        # run intake slowly
        self.interface.get_intake_forward().whileTrue(Intake_Run(self.intake, 0.25))
        # run intake full forward
        self.interface.get_intake_full().whileTrue(Intake_Run(self.intake, 1.0))
        # run intake reverse slowly
        self.interface.get_intake_reverse().whileTrue(Intake_Run(self.intake, -0.25))

        # make shooter go full speed
        self.interface.get_spin_shooter().whileTrue(Shoot(self.shooter))

        # field based triggers
        # formatter kind of makes this disgusting to read
        # basically, red and white when red
        # blue and white when blue
        # set brake on enable
        # set coast on disable
        # (different order than above)
        Trigger(lambda: DriverStation.isEnabled()).onTrue(
            self.drivetrain.set_drive_idle_command(False)
        ).onTrue(self.drivetrain.set_turn_idle_command(False)).onTrue(
            LED_Chase(
                self.led,
                (255, 255, 255),
                (
                    (
                        255
                        if DriverStation.getAlliance() == DriverStation.Alliance.kRed
                        else 0
                    ),
                    0,
                    (
                        255
                        if DriverStation.getAlliance() == DriverStation.Alliance.kBlue
                        else 0
                    ),
                ),
                40,
            )
        ).onFalse(
            self.drivetrain.set_drive_idle_command(True)
        ).onFalse(
            self.drivetrain.set_turn_idle_command(True)
        )
