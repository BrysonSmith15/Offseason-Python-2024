from commands2.button import CommandJoystick, Trigger
from wpimath import applyDeadband

"""

"""


class Interface:
    """
    This class acts as a way to safeguard for if only one controller is open
    It protects from broken usb adapters, etc
    the robotcontainer should read from this class, not the joysticks themselves
    """

    def __init__(self) -> None:
        self.driver_controller = CommandJoystick(0)
        self.operator_controller = CommandJoystick(1)

        if not self.operator_controller.getHID().isConnected():
            self.operator_controller = None

        try:
            if not self.driver_controller.getHID().isConnected():
                if self.operator_controller.getHID().isConnected():
                    self.driver_controller = self.operator_controller
                else:
                    print("No driver Controller")
                    exit(0)
        except Exception:
            pass

        self.a_button = 1
        self.b_button = 2
        self.x_button = 3
        self.y_button = 4
        self.lb_button = 5
        self.rb_button = 6
        self.back_button = 7
        self.start_button = 8
        self.left_push = 9
        self.right_push = 10

        # TODO: Make Good Values
        self.lx_axis = 0
        self.ly_axis = 1
        self.rx_axis = 4
        self.ry_axis = 5
        self.lt_axis = 2
        self.rt_axis = 3

        self.deadband = 0.1

    def periodic(self):
        if not self.driver_controller:
            try:
                self.driver_controller = CommandJoystick(0)
            except Exception:
                print("Still no driver controller")
        if not self.operator_controller:
            try:
                self.operator_controller = CommandJoystick(1)
            except Exception:
                print("Still no operator controller")

    def tmp_get_drive_top_left(self) -> Trigger:
        return self.driver_controller.button(self.a_button)

    def get_drive_forward(self) -> float:
        return (
            applyDeadband(
                -self.driver_controller.getRawAxis(self.ly_axis), self.deadband
            )
            if self.driver_controller
            else 0.0
        )

    def get_drive_side(self) -> float:
        return (
            applyDeadband(
                -self.driver_controller.getRawAxis(self.lx_axis), self.deadband
            )
            if self.driver_controller
            else 0.0
        )

    def get_drive_turn(self) -> float:
        return (
            applyDeadband(
                -self.driver_controller.getRawAxis(self.rx_axis), self.deadband
            )
            if self.driver_controller
            else 0.0
        )

    def get_drive_holonomic_forward(self) -> float:
        return (
            applyDeadband(
                self.driver_controller.getRawAxis(self.ry_axis), self.deadband
            )
            if self.driver_controller
            else 0.0
        )

    def get_drive_field_oriented(self) -> Trigger:
        return (
            Trigger(lambda: self.driver_controller.getRawAxis(self.rt_axis) < 0.25)
            if self.driver_controller
            else Trigger(lambda: False)
        )

    def get_drive_holonomic(self) -> Trigger:
        return (
            Trigger(lambda: self.driver_controller.getRawAxis(self.lt_axis) > 0.25)
            if self.driver_controller
            else Trigger(lambda: False)
        )

    def get_drive_defense_mode(self) -> Trigger:
        return (
            self.driver_controller.button(self.rb_button)
            if self.driver_controller
            else Trigger(lambda: False)
        )

    def get_drive_reset_gyro(self) -> Trigger:
        return (
            self.driver_controller.button(self.lb_button)
            if self.driver_controller
            else Trigger(lambda: False)
        )

    # Operator Stuff

    def get_elevator_up(self) -> Trigger:
        if self.operator_controller:
            return self.operator_controller.button(self.start_button)
        else:
            return (
                self.driver_controller.button(self.y_button)
                if self.driver_controller
                else Trigger(lambda: False)
            )

    def get_elevator_down(self) -> Trigger:
        if self.operator_controller:
            return (
                self.operator_controller.button(self.back_button)
                if self.driver_controller
                else Trigger(lambda: False)
            )
        else:
            return (
                self.driver_controller.button(self.a_button)
                if self.driver_controller
                else Trigger(lambda: False)
            )

    def get_intake_forward(self) -> Trigger:
        if self.operator_controller:
            return (
                self.operator_controller.button(self.a_button)
                if self.driver_controller
                else Trigger(lambda: False)
            )
        else:
            return (
                self.driver_controller.pov(0)
                if self.driver_controller
                else Trigger(lambda: False)
            )

    def get_intake_reverse(self) -> Trigger:
        if self.operator_controller:
            return (
                self.operator_controller.button(self.b_button)
                if self.driver_controller
                else Trigger(lambda: False)
            )
        else:
            return (
                self.driver_controller.pov(180)
                if self.driver_controller
                else Trigger(lambda: False)
            )

    def get_spin_shooter(self) -> Trigger:
        if self.operator_controller:
            return Trigger(
                lambda: self.operator_controller.getRawAxis(self.rt_axis) > 0.15
            )
        else:
            return (
                self.driver_controller.button(self.x_button)
                if self.driver_controller
                else Trigger(lambda: False)
            )

    def get_intake_full(self) -> Trigger:
        if self.operator_controller:
            return Trigger(
                lambda: self.operator_controller.getRawAxis(self.rt_axis) > 0.85
            )
        else:
            return (
                self.driver_controller.button(self.b_button)
                if self.driver_controller
                else Trigger(lambda: False)
            )
