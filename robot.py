# TODO: insert robot code here

from wpilib import TimedRobot, run
from commands2 import Command, CommandScheduler

from RobotContainer import *


class Robot(TimedRobot):
    m_autonomousCommand: Command = None
    m_robotContainer: RobotContainer = None

    # Initialize Robot
    def robotInit(self):
        self.m_robotContainer = RobotContainer()
        wpilib.Watchdog(0.05, lambda: None).suppressTimeoutMessage(True)

    def robotPeriodic(self) -> None:
        CommandScheduler.getInstance().run()
        self.m_robotContainer.interface.periodic()

    # Autonomous Robot Functions
    def autonomousInit(self):
        self.m_autonomousCommand = self.m_robotContainer.get_auto_command()

        if self.m_autonomousCommand != None:
            self.m_autonomousCommand.schedule()

    def autonomousPeriodic(self):
        pass

    def autonomousExit(self):
        self.m_autonomousCommand.cancel()

    # Teleop Robot Functions
    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        pass

    def teleopExit(self):
        pass

    # Test Robot Functions
    def testInit(self):
        pass

    def testPeriodic(self):
        pass

    def testExit(self):
        pass

    # Disabled Robot Functions
    def disabledInit(self):
        pass

    def disabledPeriodic(self):
        pass

    def disabledExit(self):
        pass

    def SimulationPeriodic(self) -> None:
        CommandScheduler.getInstance().run()
        print("ASDFJAKSDFJSADLKFJASDLKFJAD")


# Start the Robot when Executing Code
if __name__ == "__main__":
    run(Robot)
