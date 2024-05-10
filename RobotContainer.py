import math

import wpimath.units
from commands2 import InstantCommand
from commands2.button import Trigger
from wpilib import DriverStation, SendableChooser, SmartDashboard

from commands.autos import *
from commands.drive_joystick import Drive_Joystick
from commands.elevator_bottom import Elevator_Bottom
from commands.led_chase import LED_Chase
from subsystems.drivetrain import Drivetrain
from subsystems.elevator import Elevator
from subsystems.intake import Intake
from subsystems.interface import Interface
from subsystems.leds import LEDs
from subsystems.shooter import Shooter


# import commands2.cmd


class RobotContainer:
    def __init__(self) -> None:
        self.interface = Interface()
        self.drivetrain = Drivetrain()
        self.elevator = Elevator()
        self.shooter = Shooter()
        self.intake = Intake()
        # self.vision = Vision(self.drivetrain.get_odometry)
        self.leds = LEDs(9, 80)

        self.configure_bindings()
        self.set_default_commands()

        self.auto_chooser = SendableChooser()
        self.auto_chooser.addOption("Shoot Only", Shoot_Only)
        self.auto_chooser.addOption("Shoot and Drive Left", (Shoot_And_Drive, -1))
        self.auto_chooser.addOption("Shoot and Drive Center", (Shoot_And_Drive, 0))
        self.auto_chooser.addOption("Shoot and Drive Right", (Shoot_And_Drive, 1))
        self.auto_chooser.setDefaultOption("None", Nothing)

        SmartDashboard.putData("Auto Mode", self.auto_chooser)

    def teleop_bindings(self) -> None:
        self.drivetrain.setDefaultCommand(
            Drive_Joystick(
                self.drivetrain,
                self.interface.get_drive_forward,
                self.interface.get_drive_side,
                self.interface.get_drive_holonomic_forward,
                self.interface.get_drive_turn,
                self.interface.get_drive_field_oriented().getAsBoolean,
                self.interface.get_drive_holonomic().getAsBoolean,
            )
        )

    def set_default_commands(self) -> None:
        self.leds.setDefaultCommand(
            LED_Chase(self.leds, (255, 255, 255), (255, 50, 0), 40)
        )

    def configure_bindings(self) -> None:
        # self.interface.tmp_get_drive_top_left().onTrue(
        # Drive_Around(self.drivetrain, True)
        # Drive_WPI_Path(self.drivetrain, "4 Note.wpilib.json")
        # )

        # go really fast to fight and play defense
        self.interface.get_drive_defense_mode().onTrue(
            self.drivetrain.set_max_speed_command(
                wpimath.units.feetToMeters(100.0), 50 * math.pi
            )
        ).onFalse(
            self.drivetrain.set_max_speed_command(
                wpimath.units.feetToMeters(15.0), 2 * math.pi
            )
        )
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
                self.leds,
                (255, 255, 255),
                (
                    (
                        255
                        if DriverStation.getAlliance() is None
                        else 255 if DriverStation.getAlliance().name == "kRed" else 0
                    ),
                    0,
                    (
                        50
                        if DriverStation.getAlliance() is None
                        else 255 if DriverStation.getAlliance().name == "kBlue" else 0
                    ),
                ),
                40,
            )
        ).onFalse(
            self.drivetrain.set_drive_idle_command(True)
        ).onFalse(
            self.drivetrain.set_turn_idle_command(True)
        ).onTrue(
            InstantCommand(
                lambda: SmartDashboard.putString(
                    "Alliance", str(DriverStation.getAlliance().name)
                ),
            ),
        )

    def get_auto_command(self) -> SequentialCommandGroup:
        # return Drive_Around(self.drivetrain, True)
        to_run = self.auto_chooser.getSelected()
        print(to_run)
        if to_run == Nothing:
            return Nothing()
        elif to_run == Shoot_Only:
            return Shoot_Only(self.elevator, self.intake, self.shooter)
        elif to_run[1] == -1:
            # we are on the left from the driver's perspective
            return Shoot_And_Drive(
                self.drivetrain,
                self.elevator,
                self.intake,
                self.shooter,
                Pose2d(
                    feetToMeters(3),
                    feetToMeters(41.65 / 12),
                    Rotation2d.fromDegrees(-135),
                ),
            )

        elif to_run[1] == 0:
            # we are in the center
            return Shoot_And_Drive(
                self.drivetrain,
                self.elevator,
                self.intake,
                self.shooter,
                Pose2d(feetToMeters(3), 0, Rotation2d.fromDegrees(180)),
            )
        elif to_run[1] == 1:
            # we are on the right
            return Shoot_And_Drive(
                self.drivetrain,
                self.elevator,
                self.intake,
                self.shooter,
                Pose2d(
                    feetToMeters(3),
                    -feetToMeters(41 / 65 / 12),
                    Rotation2d.fromDegrees(135),
                ),
            )
