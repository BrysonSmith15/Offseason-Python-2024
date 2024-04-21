import wpilib
from commands2 import Command
from ntcore import NetworkTableInstance
from wpimath.trajectory import TrajectoryUtil

from subsystems.drivetrain import Drivetrain


class Drive_WPI_Path(Command):
    def __init__(self, drivetrain: Drivetrain, filename: str):
        super().__init__()
        deploy_directory = (
            "\\".join(wpilib.getDeployDirectory().split("\\")[:-1]) + "\\output"
        )
        try:
            self.path = [
                state.pose
                for state in TrajectoryUtil.fromPathweaverJson(
                    f"{deploy_directory}\\{filename}"
                ).states()
            ]
        except FileNotFoundError as ex:
            print(f"{filename} auto path not found\n{ex}\n")

        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain
        self.x_pid = self.drivetrain.x_pid
        self.y_pid = self.drivetrain.y_pid
        self.t_pid = self.drivetrain.t_pid
        self.net_table = NetworkTableInstance.getDefault().getTable(
            "Drivetrain/Follow WPI Path"
        )
        self.counter = 0

    def initialize(self) -> None:
        print(self.path)
        curr_position = self.drivetrain.get_pose()
        self.x_pid.reset(curr_position.X())
        self.y_pid.reset(curr_position.Y())
        self.t_pid.reset(curr_position.rotation().radians())
        # set coast
        self.drivetrain.set_drive_idle(True)
        self.counter = 0

    def execute(self) -> None:
        position = self.drivetrain.get_pose()
        x_out = self.x_pid.calculate(measurement=position.X(), goal=self.path[0].X())
        y_out = self.y_pid.calculate(measurement=position.Y(), goal=self.path[0].Y())
        t_out = self.t_pid.calculate(
            measurement=-position.rotation().radians(),
            goal=self.path[0].rotation().radians(),
        )
        self.net_table.putNumber("Goals/X (ft)", self.path[0].x_feet)
        self.net_table.putNumber("Goals/Y (ft)", self.path[0].y_feet)
        self.net_table.putNumber(
            "Goals/Theta (degrees)", self.path[0].rotation().degrees()
        )
        self.drivetrain.run_percentage(-x_out, -y_out, t_out)

    def isFinished(self) -> bool:
        position = self.drivetrain.get_pose()
        self.x_pid.calculate(measurement=position.X(), goal=self.path[0].X())
        self.y_pid.calculate(measurement=position.Y(), goal=self.path[0].Y())
        self.t_pid.calculate(
            measurement=-position.rotation().radians(),
            goal=self.path[0].rotation().radians(),
        )
        if (
            self.x_pid.atSetpoint()
            and self.y_pid.atSetpoint()
            and self.t_pid.atSetpoint()
        ):
            self.counter += 1
        else:
            self.counter = 0
        if self.counter >= 5:
            self.path.pop(0)
        print(self.path, end="\n\n")
        return len(self.path) == 0

    def end(self, interrupted: bool) -> None:
        self.drivetrain.set_drive_idle(False)
        self.drivetrain.stop()
