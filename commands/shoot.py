from commands2 import Command
from subsystems.shooter import Shooter


class Shoot(Command):
    def __init__(self, shooter: Shooter, power: float = 1.0):
        super().__init__()
        self.shooter = shooter
        self.addRequirements(shooter)
        self.power = power

    def execute(self):
        self.shooter.set_motors(self.power)

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.shooter.stop()
