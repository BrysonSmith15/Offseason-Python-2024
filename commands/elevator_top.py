from commands2 import Command

from subsystems.elevator import Elevator


class Elevator_Top(Command):
    def __init__(self, elevator: Elevator):
        super().__init__()
        self.addRequirements(elevator)
        self.elevator = elevator

    def execute(self) -> None:
        if self.elevator.get_ticks() < self.elevator.stable_ticks:
            self.elevator.set_motors(-self.elevator.up_speed)
        else:
            self.elevator.set_motors(-self.elevator.up_speed / 4)

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.elevator.set_motors(0)
