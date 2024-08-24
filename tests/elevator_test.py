"""
    This test module imports tests that come with pyfrc, and can be used
    to test basic functionality of just about any robot.
"""

from subsystems.elevator import Elevator
from wpilib.simulation import DriverStationSim
from wpilib import DigitalOutput


def test() -> None:
    DriverStationSim.setEnabled(True)
    DriverStationSim.setFmsAttached(True)
    my_elevator = Elevator()

    # top command testing
    # going up but already at the top
    my_command = my_elevator.to_top(
        end_condition=lambda: True, soft_condition=lambda _elevator: False)
    my_command.execute()
    assert my_elevator.curr_speed == 0
    assert my_command.isFinished()

    # going up but below the slow down point
    my_command = my_elevator.to_top(
        end_condition=lambda: False, soft_condition=lambda _elevator: False)
    my_command.execute()
    assert my_elevator.curr_speed == my_elevator.up_speed
    assert not my_command.isFinished()

    # going up, at top, and beyond slowing down point
    my_command = my_elevator.to_top(
        end_condition=lambda: True, soft_condition=lambda _elevator: True)
    my_command.execute()
    assert my_elevator.curr_speed == 0
    assert my_command.isFinished()

    # going up, not at top, and beyond slowing down point
    my_command = my_elevator.to_top(
        end_condition=lambda: False, soft_condition=lambda _elevator: True)
    my_command.execute()
    assert my_elevator.curr_speed < my_elevator.up_speed
    assert not my_command.isFinished()

    # bottom command testing
    # going down but already at the bottom
    my_command = my_elevator.to_bottom(
        end_condition=lambda: True, soft_condition=lambda _elevator: False)
    my_command.execute()
    assert my_elevator.curr_speed == 0
    assert my_command.isFinished()

    # going down but above the slow down point
    my_command = my_elevator.to_bottom(
        end_condition=lambda: False, soft_condition=lambda _elevator: False)
    my_command.execute()
    assert my_elevator.curr_speed == my_elevator.down_speed
    assert not my_command.isFinished()

    # going down, at bottom, and beyond slowing down point
    my_command = my_elevator.to_bottom(
        end_condition=lambda: True, soft_condition=lambda _elevator: True)
    my_command.execute()
    assert my_elevator.curr_speed == 0
    assert my_command.isFinished()

    # going down, not at bottom, and beyond slowing down point
    my_command = my_elevator.to_bottom(
        end_condition=lambda: False, soft_condition=lambda _elevator: True)
    my_command.execute()
    assert my_elevator.curr_speed == my_elevator.soft_down_speed
    assert not my_command.isFinished()

    # testing manual control
    # safe to go up and down, going up
    test_speed = 0.5
    my_command = my_elevator.manual_control(
        top_condition=lambda: False,
        bottom_condition=lambda: False,
        speed_control=lambda: test_speed
    )
    my_command.execute()
    assert not my_command.isFinished()
    assert my_elevator.curr_speed == test_speed

    # safe to go up and down and going down
    my_command = my_elevator.manual_control(
        top_condition=lambda: False,
        bottom_condition=lambda: False,
        speed_control=lambda: -test_speed
    )
    my_command.execute()
    assert my_elevator.curr_speed == -test_speed

    # safe to go up but not down and going up
    my_command = my_elevator.manual_control(
        top_condition=lambda: False,
        bottom_condition=lambda: True,
        speed_control=lambda: test_speed
    )
    my_command.execute()
    assert my_elevator.curr_speed == test_speed

    # safe to go down but not up and going up
    my_command = my_elevator.manual_control(
        top_condition=lambda: True,
        bottom_condition=lambda: False,
        speed_control=lambda: test_speed
    )
    my_command.execute()
    assert my_elevator.curr_speed == 0

    # TODO: figure out simulation for the DIO ports
    # test the default limit switch readers
    # top_limit_out = DigitalOutput(my_elevator.bot_limit.getChannel())
    # top_limit_out.set(False)
    # assert not my_elevator.top_pressed()
    # top_limit_out.set(True)
    # assert my_elevator.top_pressed()

    # bottom_limit_out = DigitalOutput(my_elevator.bot_limit.getChannel())
    # bottom_limit_out.set(False)
    # assert not my_elevator.bottom_pressed()
    # bottom_limit_out.set(True)
    # assert my_elevator.bottom_pressed()
