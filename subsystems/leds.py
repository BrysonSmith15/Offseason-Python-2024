from commands2 import Command, Subsystem
from wpilib import AddressableLED


class LEDs(Subsystem):
    def __init__(self, pwm_id: int, strip_len: int) -> None:
        super().__init__()
        self.strip_len = strip_len
        self.led = AddressableLED(pwm_id)
        self.led.setLength(self.strip_len)
        self.data = [AddressableLED.LEDData() for _i in range(0, strip_len)]
        self.led.setData(self.data)
        self.led.start()

    def set(self, start: int, end: int, r: int, g: int, b: int) -> None:
        for i in range(start, end):
            self.data[i].setRGB(r, g, b)

    def set_command(self, r: int, g: int, b: int) -> Command:
        return self.runOnce(self.set(0, self.strip_len, r, g, b))
