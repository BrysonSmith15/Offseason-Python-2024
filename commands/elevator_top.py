from commands2 import Command
from subsystems.elevator import Elevator

from constants import elevator_constants


class Elevator_Top(Command):
    def __init__(self, elevator: Elevator):
        super().__init__()
        self.addRequirements(elevator)
        self.elevator = elevator

    def initialize(self) -> None:
        pass

    def execute(self) -> None:
        if (
            self.elevator.get_ticks()
            < elevator_constants.stable_ticks + self.elevator.tick_offset
        ):
            self.elevator.set_motors(-elevator_constants.speed)
        elif self.elevator.top_pressed():
            self.elevator.set_motors(-elevator_constants.speed / 4)
        else:
            self.elevator.set_motors(-elevator_constants.stable_up_speed)

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.elevator.set_motors(0)
