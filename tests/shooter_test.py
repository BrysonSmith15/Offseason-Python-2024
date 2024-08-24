from subsystems.shooter import Shooter


def test():
    my_shooter = Shooter()

    my_shooter.shoot(lambda: 1.0).execute()
    assert my_shooter.curr_speed == 1.0
    my_shooter.shoot(lambda: 0.5).execute()
    assert my_shooter.curr_speed == 0.5
    my_shooter.stop().execute()
    assert my_shooter.curr_speed == 0
