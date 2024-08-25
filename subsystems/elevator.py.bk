from commands2 import Subsystem, FunctionalCommand
from ntcore import NetworkTableInstance
from rev import CANSparkLowLevel, CANSparkMax
from wpilib import DigitalInput, Encoder, RobotBase
from wpimath.filter import SlewRateLimiter
import typing


class Elevator(Subsystem):
    def __init__(self):
        super().__init__()
        self.setName("Elevator")
        self.network_table = NetworkTableInstance.getDefault().getTable("Elevator")

        self.up_speed = 0.45
        self.down_speed = 0.0
        self.soft_down_speed = 0.1
        self.curr_speed = 0
        self.network_table.putNumber("Up Speed", self.up_speed)
        self.network_table.putNumber("Down Speed", self.down_speed)
        self.network_table.putNumber("Soft Down Speed", self.soft_down_speed)

        self.stable_ticks = 650
        self.network_table.putNumber("Stable Ticks", self.stable_ticks)

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
            motor.setPeriodicFramePeriod(
                CANSparkLowLevel.PeriodicFrame.kStatus2,
                500
            )
            motor.setPeriodicFramePeriod(
                CANSparkLowLevel.PeriodicFrame.kStatus3,
                500
            )
            motor.setPeriodicFramePeriod(
                CANSparkLowLevel.PeriodicFrame.kStatus4,
                500
            )
            motor.setPeriodicFramePeriod(
                CANSparkLowLevel.PeriodicFrame.kStatus5,
                500
            )
            motor.setPeriodicFramePeriod(
                CANSparkLowLevel.PeriodicFrame.kStatus6,
                500
            )
            motor.setInverted(True)

        self.encoder.setReverseDirection(True)

        self.tick_offset = 0

    def top_pressed(self) -> bool:
        return self.top_limit.get()

    def bottom_pressed(self) -> bool:
        return self.bot_limit.get()

    def set_motors(self, power: float) -> None:
        if (
            RobotBase.isReal() and
            ((power > 0 and self.top_pressed())
             or (power < 0 and self.bottom_pressed())
             or power == 0)
        ):
            power = 0
        else:
            power = 1 if power > 1 else -1 if power < -1 else power
            if RobotBase.isReal():
                power = self.rate_limiter.calculate(power)
        self.curr_speed = power
        self.motor_l1.set(power)

    def get_ticks(self) -> int:
        return self.encoder.get()

    def to_top(self, *,
               end_condition: typing.Callable[[], bool] = top_pressed,
               soft_condition: typing.Callable[[], bool] =
               lambda self: self.get_ticks() < self.stable_ticks
               ) -> FunctionalCommand:
        assert callable(end_condition)
        assert callable(soft_condition)
        out = FunctionalCommand(
            onInit=lambda: self.set_motors(0),
            onExecute=lambda: self.set_motors(
                0 if end_condition() else
                self.up_speed / 4 if soft_condition(self) else
                self.up_speed),
            onEnd=lambda _interrupted: self.set_motors(0),
            isFinished=end_condition
        )
        out.addRequirements(self)
        return out

    def to_bottom(
        self, *,
        end_condition: typing.Callable[[], bool] = bottom_pressed,
        soft_condition: typing.Callable[[
        ], bool] = lambda self: self.get_ticks() < self.stable_ticks
    ) -> FunctionalCommand:
        assert callable(end_condition)
        assert callable(soft_condition)

        out = FunctionalCommand(
            onInit=lambda: self.set_motors(0),
            onExecute=lambda: self.set_motors(
                0 if end_condition() else
                self.soft_down_speed if soft_condition(self) else
                self.down_speed),
            onEnd=lambda _interrupted: self.set_motors(0),
            isFinished=end_condition
        )
        out.addRequirements(self)
        return out

    def manual_control(
        self, *,
        speed_control: typing.Callable[[], float],
        top_condition: typing.Callable[[], bool] = top_pressed,
        bottom_condition: typing.Callable[[], bool] = bottom_pressed,
    ) -> FunctionalCommand:
        assert callable(top_condition)
        assert callable(bottom_condition)
        assert callable(speed_control)

        out = FunctionalCommand(
            onInit=lambda: self.set_motors(0),
            onExecute=lambda: self.set_motors(speed_control() if not (
                top_condition() and speed_control() >= 0
            ) or (
                bottom_condition() and speed_control() <= 0) else 0
            ),
            onEnd=lambda _interrupted: self.set_motors(0),
            isFinished=lambda: (top_condition() and speed_control() >= 0) or (
                bottom_condition() and speed_control() <= 0)
        )
        out.addRequirements(self)
        return out

    def periodic(self) -> None:
        if self.bottom_pressed():
            self.encoder.reset()
        self.network_table.putNumber("Encoder Ticks", self.get_ticks())
        self.network_table.putNumber("Speed", self.motor_l1.get())
        self.up_speed = self.network_table.getNumber("Up Speed", self.up_speed)
        self.down_speed = self.network_table.getNumber(
            "Down Speed", self.down_speed)
        self.soft_down_speed = self.network_table.getNumber(
            "Soft Down Speed", self.soft_down_speed
        )
        self.stable_ticks = self.network_table.getNumber(
            "Stable Ticks", self.stable_ticks
        )
