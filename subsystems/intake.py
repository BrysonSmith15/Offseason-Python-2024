from commands2 import Subsystem
from wpimath.filter import SlewRateLimiter

from rev import CANSparkLowLevel
from rev import CANSparkMax


class Intake(Subsystem):
    def __init__(self) -> None:
        super().__init__()
        self.motor = CANSparkMax(23, CANSparkLowLevel.MotorType.kBrushless)
        self.limiter = SlewRateLimiter(1 / 2)

        self.setName("Intake")
        self.addChild("Motor", self.motor)

    def set_motor(self, power: float) -> None:
        power = 1 if power > 1 else -1 if power < -1 else power
        self.motor.set(self.limiter.calculate(power))

    def stop(self) -> None:
        self.motor.set(0)
