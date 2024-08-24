from commands2 import Subsystem, FunctionalCommand, InterruptionBehavior, InstantCommand
from rev import CANSparkLowLevel, CANSparkMax
from wpimath.filter import SlewRateLimiter
from wpilib import RobotBase
import typing


class Intake(Subsystem):
    def __init__(self) -> None:
        super().__init__()
        self.motor = CANSparkMax(23, CANSparkLowLevel.MotorType.kBrushless)
        self.limiter = SlewRateLimiter(1 / 2)

        self.setName("Intake")

        self.curr_speed: float = 0

        self.motor.setPeriodicFramePeriod(
            CANSparkLowLevel.PeriodicFrame.kStatus2, 500)
        self.motor.setPeriodicFramePeriod(
            CANSparkLowLevel.PeriodicFrame.kStatus3, 500)
        self.motor.setPeriodicFramePeriod(
            CANSparkLowLevel.PeriodicFrame.kStatus4, 500)
        self.motor.setPeriodicFramePeriod(
            CANSparkLowLevel.PeriodicFrame.kStatus5, 500)
        self.motor.setPeriodicFramePeriod(
            CANSparkLowLevel.PeriodicFrame.kStatus6, 500)

    def set_motor(self, power: float) -> None:
        power = 1 if power > 1 else -1 if power < -1 else power
        if RobotBase.isReal():
            power = self.limiter.calculate(power)
        self.motor.set(self.limiter.calculate(power))
        self.curr_speed = power

    def run_motor(
        self, *,
        speed: typing.Callable[[], float],
        can_run=lambda: True
    ) -> FunctionalCommand:
        assert callable(speed)
        assert callable(can_run)
        out = FunctionalCommand(
            onInit=lambda: self.set_motor(0),
            onExecute=lambda: self.set_motor(speed() if can_run() else 0),
            isFinished=lambda: False,
            onEnd=lambda _interrupted: self.set_motor(0),
        ).withInterruptBehavior(InterruptionBehavior.kCancelSelf)
        out.addRequirements(self)
        return out

    def full_intake(self) -> FunctionalCommand:
        return self.run_motor(speed=lambda: 1.0)

    def slow_intake(self) -> FunctionalCommand:
        return self.run_motor(speed=lambda: 0.1)

    def reverse_intake(self) -> FunctionalCommand:
        return self.run_motor(speed=lambda: -0.25)

    def stop(self) -> FunctionalCommand:
        out = FunctionalCommand(
            onInit=self._stop,
            onExecute=self._stop,
            isFinished=lambda: self.curr_speed == 0,
            onEnd=self._stop,
        )
        out.addRequirements(self)
        return out

    def _stop(self) -> None:
        self.set_motor(0)
