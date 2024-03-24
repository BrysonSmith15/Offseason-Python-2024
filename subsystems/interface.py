import commands2.button
from wpimath import applyDeadband
from commands2.button import Trigger


class Interface:
    """
    This class acts as a way to safeguard for if only one controller is open
    It protects from broken usb adapters, etc
    the robotcontainer should read from this class, not the joysticks themselves
    """

    def __init__(self) -> None:
        self.driver_controller = commands2.button.CommandGenericHID(0)
        try:
            self.operator_controller = commands2.button.CommandGenericHID(1)
        except Exception as ex:
            self.operator_controller = None
            print(f"Error getting operator controller, mapping all to driver: {ex}")

        self.a_button = 0
        self.b_button = 0
        self.x_button = 0
        self.y_button = 0
        self.lb_button = 0
        self.rb_button = 0
        self.start_button = 0
        self.back_button = 0
        self.left_push = 0
        self.right_push = 0

        self.lx_axis = 1
        self.ly_axis = 0
        self.rx_axis = 3
        self.ry_axis = 4
        self.lt_axis = 0
        self.rt_axis = 0

        self.deadband = 0.1

    def get_drive_forward(self) -> float:
        return applyDeadband(
            self.driver_controller.getRawAxis(self.lx_axis), self.deadband
        )

    def get_drive_side(self) -> float:
        return applyDeadband(
            self.driver_controller.getRawAxis(self.ly_axis), self.deadband
        )

    def get_drive_turn(self) -> float:
        return applyDeadband(
            self.driver_controller.getRawAxis(self.rx_axis), self.deadband
        )

    def get_drive_holonomic_forward(self) -> float:
        return applyDeadband(
            self.driver_controller.getRawAxis(self.ry_axis), self.deadband
        )

    def get_drive_field_oriented(self) -> Trigger:
        return Trigger(lambda: self.driver_controller.getRawAxis(self.rt_axis) < 0.25)

    def get_drive_holonomic(self) -> Trigger:
        return Trigger(lambda: self.driver_controller.getRawAxis(self.rt_axis) < 0.25)

    def get_drive_defense_mode(self) -> Trigger:
        return self.driver_controller.button(self.rb_button)

    def get_drive_reset_gyro(self) -> Trigger:
        return self.driver_controller.button(self.lb_button)
