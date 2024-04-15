from commands2 import Subsystem
from ntcore import NetworkTableInstance
from rev import CANSparkLowLevel, CANSparkMax
from wpilib import DigitalInput, Encoder
from wpimath.filter import SlewRateLimiter


class Elevator(Subsystem):
    def __init__(self):
        super().__init__()
        self.setName("Elevator")
        self.network_table = NetworkTableInstance.getDefault().getTable("Elevator")

        self.motor_l1 = CANSparkMax(26, CANSparkLowLevel.MotorType.kBrushed)
        self.motor_l2 = CANSparkMax(27, CANSparkLowLevel.MotorType.kBrushed)
        self.motor_r1 = CANSparkMax(24, CANSparkLowLevel.MotorType.kBrushed)
        self.motor_r2 = CANSparkMax(25, CANSparkLowLevel.MotorType.kBrushed)

        self.motor_l2.follow(self.motor_l1, False)
        self.motor_r1.follow(self.motor_l1, True)
        self.motor_r2.follow(self.motor_l1, True)

        self.rate_limiter = SlewRateLimiter(2)

        self.top_limit = DigitalInput(0)
        self.bot_limit = DigitalInput(1)

        self.encoder = Encoder(8, 9)

        motors = [self.motor_l1, self.motor_l2, self.motor_r1, self.motor_r2]
        for motor in motors:
            motor.setPeriodicFramePeriod(CANSparkLowLevel.PeriodicFrame.kStatus2, 500)
            motor.setPeriodicFramePeriod(CANSparkLowLevel.PeriodicFrame.kStatus3, 500)
            motor.setPeriodicFramePeriod(CANSparkLowLevel.PeriodicFrame.kStatus4, 500)
            motor.setPeriodicFramePeriod(CANSparkLowLevel.PeriodicFrame.kStatus5, 500)
            motor.setPeriodicFramePeriod(CANSparkLowLevel.PeriodicFrame.kStatus6, 500)

        self.encoder.setReverseDirection(True)

        self.tick_offset = 0

    def top_pressed(self) -> bool:
        return self.top_limit.get()

    def bot_pressed(self) -> bool:
        return self.bot_limit.get()

    def set_motors(self, power: float) -> None:
        power = -power
        if (
            (power > 0 and self.top_pressed())
            or (power < 0 and self.bot_pressed())
            or power == 0
        ):
            power = 0
        else:
            power = 1 if power > 1 else -1 if power < -1 else power
            power = self.rate_limiter.calculate(power)
        self.motor_l1.set(power)

    def get_ticks(self) -> int:
        return self.encoder.get()

    def periodic(self) -> None:
        if self.bot_pressed():
            self.encoder.reset()
        self.network_table.putNumber("Encoder Ticks", self.get_ticks())
