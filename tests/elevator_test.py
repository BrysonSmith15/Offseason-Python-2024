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

    # test the default limit switch readers
    top_limit_out = DigitalOutput(my_elevator.bot_limit.getChannel())
    top_limit_out.set(False)
    assert not my_elevator.top_pressed()
    top_limit_out.set(True)
    assert my_elevator.top_pressed()

    # TODO: figure out simulation for the DIO ports
    # bottom_limit_out = DigitalOutput(my_elevator.bot_limit.getChannel())
    # bottom_limit_out.set(False)
    # assert not my_elevator.bottom_pressed()
    # bottom_limit_out.set(True)
    # assert my_elevator.bottom_pressed()
