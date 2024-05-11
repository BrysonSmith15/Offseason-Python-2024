from commands2 import Command

from subsystems.elevator import Elevator


class Elevator_Bottom(Command):
    def __init__(self, elevator: Elevator):
        super().__init__()
        self.addRequirements(elevator)
        self.elevator = elevator

    def execute(self) -> None:
        if self.elevator.get_ticks() < self.elevator.stable_ticks:
            self.elevator.set_motors(self.elevator.soft_down_speed)
        else:
            self.elevator.set_motors(self.elevator.down_speed)

    def isFinished(self) -> bool:
        return self.elevator.bot_pressed()

    def end(self, interrupted: bool):
        self.elevator.set_motors(0)
