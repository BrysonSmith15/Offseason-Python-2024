from commands2 import Command
from subsystems.intake import Intake


class Intake_Run(Command):
    def __init__(self, intake: Intake, power: float):
        super().__init__()
        self.intake = intake
        self.power = power
        self.addRequirements(intake)

    def execute(self):
        self.intake.set_motor(self.power)

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.intake.stop()
