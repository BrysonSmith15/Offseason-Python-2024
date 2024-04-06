from commands2 import Command
from subsystems.leds import LEDs
from typing import Tuple


class LED_Chase(Command):
    def __init__(
        self,
        leds: LEDs,
        main_color: Tuple[int, int, int],
        chase_color: Tuple[int, int, int],
        chase_width: int,
    ):
        super().__init__()
        self.main_color = main_color
        self.chase_color = chase_color
        self.chase_width = chase_width
        self.counter = 0
        self.chase_point = 0
        self.led = leds
        self.addRequirements(leds)

    def initialize(self):
        self.counter = 0
        self.chase_point = 0

    def execute(self):
        self.counter += 1
        if self.counter % 1 == 0:
            self.chase_point += 1
            self.chase_point %= self.led.strip_len
        chase_end: int = self.chase_point + self.chase_width
        if chase_end > self.led.strip_len:
            self.led.set(
                self.chase_point,
                self.led.strip_len,
                self.chase_color[0],
                self.chase_color[1],
                self.chase_color[2],
            )
            self.led.set(
                0,
                chase_end - self.led.strip_len,
                self.chase_color[0],
                self.chase_color[1],
                self.chase_color[2],
            )
            self.led.set(
                chase_end - self.led.strip_len + 1,
                self.chase_point,
                self.chase_color[0],
                self.chase_color[1],
                self.chase_color[2],
            )
        else:
            self.led.set(
                0,
                self.led.strip_len,
                self.main_color[0],
                self.main_color[1],
                self.main_color[2],
            )
            self.led.set(
                self.chase_point,
                chase_end,
                self.chase_color[0],
                self.chase_color[1],
                self.chase_color[2],
            )

    def end(self, interrupted: bool):
        self.led.set(
            0,
            self.led.strip_len,
            self.main_color[0],
            self.main_color[1],
            self.main_color[2],
        )

    def isFinished(self) -> bool:
        return False

    def runsWhenDisabled(self) -> bool:
        return True
