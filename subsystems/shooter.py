from commands2 import Subsystem
from rev import CANSparkLowLevel, CANSparkMax
from wpimath.filter import SlewRateLimiter


class Shooter(Subsystem):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Shooter"

        self.motor_l1 = CANSparkMax(21, CANSparkLowLevel.MotorType.kBrushed)
        # self.motor_l2 = CANSparkMax(21, CANSparkLowLevel.MotorType.kBrushed)
        self.motor_r1 = CANSparkMax(30, CANSparkLowLevel.MotorType.kBrushed)
        # self.motor_r2 = CANSparkMax(21, CANSparkLowLevel.MotorType.kBrushed)

        self.rate_limiter = SlewRateLimiter(4)

        # self.motor_l2.follow(self.motor_l1, False)
        self.motor_r1.follow(self.motor_l1, True)
        # self.motor_r2.follow(self.motor_l1, True)

        for motor in [self.motor_l1, self.motor_r1]:
            motor.setPeriodicFramePeriod(CANSparkLowLevel.PeriodicFrame.kStatus2, 100)
            motor.setPeriodicFramePeriod(CANSparkLowLevel.PeriodicFrame.kStatus3, 100)
            motor.setPeriodicFramePeriod(CANSparkLowLevel.PeriodicFrame.kStatus4, 100)
            motor.setPeriodicFramePeriod(CANSparkLowLevel.PeriodicFrame.kStatus5, 100)
            motor.setPeriodicFramePeriod(CANSparkLowLevel.PeriodicFrame.kStatus6, 100)

    def set_motors(self, power: float) -> None:
        power = 1 if power > 1 else -1 if power < -1 else power
        self.motor_l1.set(power)

    def stop(self) -> None:
        self.motor_l1.set(0)
