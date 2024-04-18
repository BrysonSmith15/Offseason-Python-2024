import math

from commands2 import InstantCommand, Subsystem
from hal import SerialPort
from navx import AHRS
from ntcore import NetworkTableInstance
from wpilib import DriverStation, Field2d, RobotBase, SmartDashboard, Timer
from wpilib._wpilib import SerialPort
from wpimath.controller import ProfiledPIDController
from wpimath.estimator import SwerveDrive4PoseEstimator
from wpimath.filter import SlewRateLimiter
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.kinematics import ChassisSpeeds, SwerveDrive4Kinematics
from wpimath.trajectory import TrapezoidProfile
from wpimath.units import degreesToRadians, feetToMeters, inchesToMeters

from subsystems.swerve_module import SwerveModule


class Drivetrain(Subsystem):
    __ntTbl__ = NetworkTableInstance.getDefault().getTable("Drivetrain")

    def __init__(self):
        super().__init__()

        # MPS
        self.maxVelocity = feetToMeters(15)
        # RAD / S
        self.maxAngularVelocity = 2 * math.pi
        # accel time (seconds)
        self.time_to_max_velocity = 1

        self.setName("Drivetrain")
        self.chassis_speeds = ChassisSpeeds(0, 0, 0)
        self.is_real = RobotBase.isReal()

        self.robotName = "Robot"
        self.gyro = AHRS(SerialPort.Port.kUSB1)

        self.fl = SwerveModule("fl", 14, 12, 13, True, True)
        self.fr = SwerveModule("fr", 11, 9, 10, False, True)
        self.bl = SwerveModule("bl", 17, 15, 16, True, False)
        self.br = SwerveModule("br", 8, 6, 7, False, False)

        self.kinematics = SwerveDrive4Kinematics(
            self.fl.getModulePosition(),
            self.fr.getModulePosition(),
            self.bl.getModulePosition(),
            self.br.getModulePosition(),
        )

        self.odometry = SwerveDrive4PoseEstimator(
            self.kinematics,
            self.gyro.getRotation2d(),
            (
                self.fl.getPosition(),
                self.fr.getPosition(),
                self.bl.getPosition(),
                self.br.getPosition(),
            ),
            Pose2d(Translation2d(), Rotation2d().fromDegrees(0)),
        )
        self.odometry.setVisionMeasurementStdDevs((0.1, 0.1, math.pi / 8))

        self.x_limiter = SlewRateLimiter(self.maxVelocity / self.time_to_max_velocity)
        self.y_limiter = SlewRateLimiter(self.maxVelocity / self.time_to_max_velocity)
        self.t_limiter = SlewRateLimiter(
            self.maxAngularVelocity / self.time_to_max_velocity,
            -4 * self.maxAngularVelocity / self.time_to_max_velocity,
        )

        self.x_pid = ProfiledPIDController(
            3e-1,
            0,
            1e-7,
            TrapezoidProfile.Constraints(
                self.maxVelocity, self.maxVelocity / self.time_to_max_velocity
            ),
        )
        self.y_pid = ProfiledPIDController(
            3e-1,
            0,
            1e-7,
            TrapezoidProfile.Constraints(
                self.maxVelocity, 2 * self.maxVelocity / self.time_to_max_velocity
            ),
        )
        self.t_pid = ProfiledPIDController(
            5e-1,
            0,
            1e-2,
            TrapezoidProfile.Constraints(
                self.maxAngularVelocity,
                self.maxAngularVelocity / self.time_to_max_velocity,
            ),
        )

        self.x_pid.setTolerance(inchesToMeters(3))
        self.y_pid.setTolerance(inchesToMeters(3))
        self.t_pid.setTolerance(degreesToRadians(3))
        self.t_pid.enableContinuousInput(-math.pi, math.pi)

        SmartDashboard.putData("Field", Field2d())

    def periodic(self):
        pose = self.odometry.updateWithTime(
            Timer.getFPGATimestamp(),
            self.gyro.getRotation2d(),
            (
                self.fl.getPosition(),
                self.fr.getPosition(),
                self.bl.getPosition(),
                self.br.getPosition(),
            ),
        )
        self.__ntTbl__.putString("Running Command", str(self.getCurrentCommand()))
        if not self.is_real:
            self.odometry.resetPosition(
                self.get_angle(),
                (
                    self.fl.getPosition(),
                    self.fr.getPosition(),
                    self.bl.getPosition(),
                    self.br.getPosition(),
                ),
                Pose2d(
                    Translation2d(
                        pose.X() + self.chassis_speeds.vx / 50,
                        pose.Y() + self.chassis_speeds.vy / 50,
                    ),
                    Rotation2d(
                        pose.rotation().radians() - self.chassis_speeds.omega / 50
                    ),
                ),
            )
            self.__ntTbl__.putNumber(
                "ChassisSpeeds vx (fps)", self.chassis_speeds.vx_fps
            )
            self.__ntTbl__.putNumber(
                "ChassisSpeeds vy (fps)", self.chassis_speeds.vy_fps
            )
            self.__ntTbl__.putNumber(
                "ChassisSpeeds omega (rad/s)", self.chassis_speeds.omega
            )

        poseX = round(pose.X(), 3)
        poseY = round(pose.Y(), 3)
        poseT = round(pose.rotation().degrees(), 3)

        self.__ntTbl__.putNumber("PositionX", poseX)
        self.__ntTbl__.putNumber("PositionY", poseY)
        self.__ntTbl__.putNumber("Rotation", poseT)

        x_p = self.__ntTbl__.getNumber("xPID/P", self.x_pid.getP())
        x_i = self.__ntTbl__.getNumber("xPID/I", self.x_pid.getI())
        x_d = self.__ntTbl__.getNumber("xPID/D", self.x_pid.getD())

        y_p = self.__ntTbl__.getNumber("yPID/P", self.y_pid.getP())
        y_i = self.__ntTbl__.getNumber("yPID/I", self.y_pid.getI())
        y_d = self.__ntTbl__.getNumber("yPID/D", self.y_pid.getD())

        t_p = self.__ntTbl__.getNumber("tPID/P", self.t_pid.getP())
        t_i = self.__ntTbl__.getNumber("tPID/I", self.t_pid.getI())
        t_d = self.__ntTbl__.getNumber("tPID/D", self.t_pid.getD())

        self.x_pid.setPID(x_p, x_i, x_d)
        self.y_pid.setPID(y_p, y_i, y_d)
        self.t_pid.setPID(t_p, t_i, t_d)

        if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
            poseX = feetToMeters(54) - poseX
            poseY = feetToMeters(27) - poseY
            poseT -= 180

        SmartDashboard.putNumberArray(f"Field/{self.robotName}", [poseX, poseY, poseT])

    def stop(self) -> None:
        self.run_chassis_speeds(ChassisSpeeds(0, 0, 0))

    # gets
    def get_kinematics(self) -> SwerveDrive4Kinematics:
        return self.kinematics

    def get_odometry(self) -> SwerveDrive4PoseEstimator:
        return self.odometry

    def get_pose(self) -> Pose2d:
        return self.odometry.getEstimatedPosition()

    def get_angle(self) -> Rotation2d:
        return self.gyro.getRotation2d()

    def get_module_positions(self):
        return (
            self.fl.getPosition(),
            self.fr.getPosition(),
            self.bl.getPosition(),
            self.br.getPosition(),
        )

    def reset_gyro(self) -> None:
        self.gyro.reset()

    def reset_gyro_command(self) -> InstantCommand:
        cmd = InstantCommand(lambda: self.reset_gyro(), self)
        cmd.runsWhenDisabled = lambda: True
        return cmd

    def set_drive_idle(self, coast: bool):
        self.fl.set_drive_idle(coast)
        self.fr.set_drive_idle(coast)
        self.bl.set_drive_idle(coast)
        self.br.set_drive_idle(coast)

    def set_drive_idle_command(self, coast: bool):
        cmd = InstantCommand(lambda: self.set_drive_idle(coast), self)
        cmd.runsWhenDisabled = lambda: True
        return cmd

    def set_turn_idle(self, coast: bool):
        self.fl.set_turn_idle(coast)
        self.fr.set_turn_idle(coast)
        self.bl.set_turn_idle(coast)
        self.br.set_turn_idle(coast)

    def set_turn_idle_command(self, coast: bool):
        cmd = InstantCommand(lambda: self.set_turn_idle(coast), self)
        cmd.runsWhenDisabled = lambda: True
        return cmd

    def set_max_speed(self, speed: float, turn_speed: float) -> None:
        self.maxVelocity = speed
        self.maxAngularVelocity = turn_speed

    def set_max_speed_command(self, speed: float, turn_speed: float) -> InstantCommand:
        return InstantCommand(lambda: self.set_max_speed(speed, turn_speed), self)

    # drive
    def run_percentage(
        self,
        x: float = 0.0,
        y: float = 0.0,
        theta: float = 0.0,
        field_relative: bool = True,
    ) -> None:
        # vX = self.x_limiter.calculate(x * maxVelocity)
        # vY = self.y_limiter.calculate(y * maxVelocity)
        # vT = self.t_limiter.calculate(theta * maxAngularVelocity)
        vX = x * self.maxVelocity
        vY = y * self.maxVelocity
        vT = theta * self.maxAngularVelocity

        if field_relative:
            speeds = ChassisSpeeds.fromFieldRelativeSpeeds(
                vx=vX, vy=vY, omega=vT, robotAngle=self.get_angle()
            )
        else:
            speeds = ChassisSpeeds(vx=vX, vy=vY, omega=vT)

        self.run_chassis_speeds(speeds)

    def run_chassis_speeds(
        self,
        speeds: ChassisSpeeds,
        center_of_rotation: Translation2d = Translation2d(0, 0),
    ) -> None:
        self.chassis_speeds = speeds
        states = self.kinematics.toSwerveModuleStates(
            self.chassis_speeds, center_of_rotation
        )
        self.run_module_states(list(states))

    def run_module_states(self, states) -> None:
        states = self.kinematics.desaturateWheelSpeeds(states, self.maxVelocity)
        self.fl.setDesiredState(states[0])
        self.fr.setDesiredState(states[1])
        self.bl.setDesiredState(states[2])
        self.br.setDesiredState(states[3])
