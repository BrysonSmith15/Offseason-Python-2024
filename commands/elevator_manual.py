from commands2 import Command
import typing
from subsystems.elevator import Elevator


class Elevator_Manual(Command):
    def __init__(self, elevator: Elevator, power: float):
        super().__init__()
        self.addRequirements(elevator)
        self.elevator = elevator
        self.power = power

    def initialize(self):
        self.elevator.set_motors(self.power)

    def isFinished(self) -> bool:
        return (self.elevator.top_pressed() and self.power > 0) or (
            self.elevator.bot_pressed() and self.power < 0
        )

    def end(self, interrupted: bool):
        self.elevator.set_motors(0)
