from subsystems.intake import Intake


def test():
    my_intake = Intake()

    test_speed = 0.5
    my_command = my_intake.run_motor(speed=lambda: test_speed)
    my_command.execute()
    assert my_intake.curr_speed == test_speed

    my_command = my_intake.run_motor(
        speed=lambda: test_speed, can_run=lambda: False)
    my_command.execute()
    assert my_intake.curr_speed == 0

    my_command = my_intake.full_intake()
    my_command.execute()
    assert my_intake.curr_speed == 1
    my_intake.stop().execute()
    assert my_intake.curr_speed == 0
    my_intake.slow_intake().execute()
    assert my_intake.curr_speed == 0.1
    my_intake.stop().execute()
    assert my_intake.curr_speed == 0
    my_intake.reverse_intake().execute()
    assert my_intake.curr_speed == -0.25
    my_intake.stop().execute()
    assert my_intake.curr_speed == 0
