from commands2 import Subsystem
from rev import CANSparkLowLevel, CANSparkMax
from wpimath.filter import SlewRateLimiter


class Intake(Subsystem):
    def __init__(self) -> None:
        super().__init__()
        self.motor = CANSparkMax(23, CANSparkLowLevel.MotorType.kBrushless)
        self.limiter = SlewRateLimiter(1 / 2)

        self.setName("Intake")

        self.motor.setPeriodicFramePeriod(CANSparkLowLevel.PeriodicFrame.kStatus2, 500)
        self.motor.setPeriodicFramePeriod(CANSparkLowLevel.PeriodicFrame.kStatus3, 500)
        self.motor.setPeriodicFramePeriod(CANSparkLowLevel.PeriodicFrame.kStatus4, 500)
        self.motor.setPeriodicFramePeriod(CANSparkLowLevel.PeriodicFrame.kStatus5, 500)
        self.motor.setPeriodicFramePeriod(CANSparkLowLevel.PeriodicFrame.kStatus6, 500)

    def set_motor(self, power: float) -> None:
        power = 1 if power > 1 else -1 if power < -1 else power
        self.motor.set(self.limiter.calculate(power))

    def stop(self) -> None:
        self.motor.set(0)
