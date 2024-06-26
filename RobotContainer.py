import math

import wpimath.units
from wpimath.units import feetToMeters
from wpimath.geometry import Rotation2d, Pose2d
from commands2.button import Trigger
from commands2 import SequentialCommandGroup
from wpilib import DriverStation, SmartDashboard

# from commands.autos import Shoot_Only, Shoot_And_Drive, Nothing
from commands.drive_angle import DriveAngle
from commands.drive_joystick import Drive_Joystick
from commands.drive_translation import DriveTranslation
from commands.shoot import Shoot
from commands.elevator_top import Elevator_Top
from commands.elevator_bottom import Elevator_Bottom
from commands.led_chase import LED_Chase
from commands.intake_run import Intake_Run

from subsystems.drivetrain import Drivetrain
from subsystems.elevator import Elevator
from subsystems.intake import Intake
from subsystems.interface import Interface
from subsystems.leds import LEDs
from subsystems.shooter import Shooter

from pathplannerlib.auto import AutoBuilder, NamedCommands  # , PathPlannerAuto
# from pathplannerlib.path import GoalEndState, PathConstraints, PathPlannerPath


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

        # auto go brr
        NamedCommands.registerCommand("Shoot", Shoot(self.shooter))
        NamedCommands.registerCommand(
            "Elevator_Top", Elevator_Top(self.elevator))
        NamedCommands.registerCommand(
            "Elevator_Bottom", Elevator_Bottom(self.elevator))
        NamedCommands.registerCommand(
            "Intake_Run_In_Fast", Intake_Run(self.intake, 1.0))
        self.auto_chooser = AutoBuilder.buildAutoChooser()
        SmartDashboard.putData("Auto Mode", self.auto_chooser)

        # self.auto_chooser = SendableChooser()
        # self.auto_chooser.addOption("Shoot Only", Shoot_Only)
        # self.auto_chooser.addOption(
        #     "Shoot and Drive Left", (Shoot_And_Drive, -1))
        # self.auto_chooser.addOption(
        #     "Shoot and Drive Center", (Shoot_And_Drive, 0))
        # self.auto_chooser.addOption(
        #     "Shoot and Drive Right", (Shoot_And_Drive, 1))
        # self.auto_chooser.setDefaultOption("None", Nothing)

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

        # test drive positions
        # rotate to the front
        self.interface.tmp_rotate_forwards().onTrue(
            DriveAngle(self.drivetrain, Rotation2d.fromDegrees(0))
        )

        # rotate to the back
        self.interface.tmp_rotate_backwards().onTrue(
            DriveAngle(self.drivetrain, Rotation2d.fromDegrees(180))
        )

        # drive 1 ft forwards
        self.interface.tmp_drive_forwards().onTrue(
            DriveTranslation(self.drivetrain, Pose2d(
                feetToMeters(5), 0, Rotation2d(0)))
        )

        # drive 1 ft backwards
        self.interface.tmp_drive_forwards().onTrue(
            DriveTranslation(
                self.drivetrain, Pose2d(-feetToMeters(5), 0, Rotation2d(0))
            )
        )

        # move shooter to the top
        self.interface.get_elevator_up().onTrue(
            Elevator_Top(self.elevator)
        )

        # move shooter to the bottom
        self.interface.get_elevator_down().onTrue(
            Elevator_Bottom(self.elevator)
        )

        # run intake slowly
        self.interface.get_intake_forward().whileTrue(
            Intake_Run(self.intake, 0.25)
        )
        # run intake full forward
        self.interface.get_intake_full().whileTrue(
            Intake_Run(self.intake, 1.0)
        )
        # run intake reverse slowly
        self.interface.get_intake_reverse().whileTrue(
            Intake_Run(self.intake, -0.25)
        )

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
        )

    def get_auto_command(self) -> SequentialCommandGroup:
        return self.auto_chooser.getSelected()
