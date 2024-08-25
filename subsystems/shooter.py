from commands2 import Subsystem, FunctionalCommand, InstantCommand
from rev import CANSparkLowLevel, CANSparkMax
from wpimath.filter import SlewRateLimiter
from wpilib import RobotBase
import typing


class Shooter(Subsystem):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Shooter"

        self.motor_l1 = CANSparkMax(21, CANSparkLowLevel.MotorType.kBrushed)
        # self.motor_l2 = CANSparkMax(21, CANSparkLowLevel.MotorType.kBrushed)
        self.motor_r1 = CANSparkMax(30, CANSparkLowLevel.MotorType.kBrushed)
        # self.motor_r2 = CANSparkMax(21, CANSparkLowLevel.MotorType.kBrushed)

        self.rate_limiter = SlewRateLimiter(4)

        self.curr_speed: float = 0

        # self.motor_l2.follow(self.motor_l1, False)
        self.motor_r1.follow(self.motor_l1, True)
        # self.motor_r2.follow(self.motor_l1, True)

        for motor in [self.motor_l1, self.motor_r1]:
            motor.setPeriodicFramePeriod(
                CANSparkLowLevel.PeriodicFrame.kStatus2, 100
            )
            motor.setPeriodicFramePeriod(
                CANSparkLowLevel.PeriodicFrame.kStatus3, 100
            )
            motor.setPeriodicFramePeriod(
                CANSparkLowLevel.PeriodicFrame.kStatus4, 100
            )
            motor.setPeriodicFramePeriod(
                CANSparkLowLevel.PeriodicFrame.kStatus5, 100
            )
            motor.setPeriodicFramePeriod(
                CANSparkLowLevel.PeriodicFrame.kStatus6, 100
            )

    def set_motors(self, power: float) -> None:
        power = 1 if power > 1 else -1 if power < -1 else power
        if RobotBase.isReal():
            power = self.rate_limiter.calculate(power)
        self.motor_l1.set(power)
        self.curr_speed = power

    def shoot(
        self, power: typing.Callable[[], float] = lambda: 1.0
    ) -> FunctionalCommand:
        out = FunctionalCommand(
            onInit=lambda: self.set_motors(0),
            onExecute=lambda: self.set_motors(power()),
            isFinished=lambda: False,
            onEnd=self.stop,
        )
        out.addRequirements(self)
        return out

    def stop(self) -> FunctionalCommand:
        out = FunctionalCommand(
            onInit=lambda: self.set_motors(0),
            onExecute=lambda: self.set_motors(0),
            isFinished=lambda: self.curr_speed == 0,
            onEnd=lambda _interrupted: self.set_motors(0),
        )
        out.addRequirements(self)
        return out

    def _stop(self) -> None:
        self.set_motors(0)
