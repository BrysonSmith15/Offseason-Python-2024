from robotpy_apriltag import AprilTagField
from commands2 import Subsystem
from photonlibpy.photonPoseEstimator import PhotonPoseEstimator, PoseStrategy
from photonlibpy.photonCamera import PhotonCamera
import typing
from wpimath.estimator import SwerveDrive4PoseEstimator
from wpimath.geometry import Transform3d, Rotation3d
from wpimath.units import inchesToMeters, degreesToRadians


class Vision(Subsystem):
    def __init__(
        self, get_odometry: typing.Callable[[], SwerveDrive4PoseEstimator]
    ) -> None:
        super().__init__()
        self.setName("Vision")
        self.subsystem("Vision")
        self.get_odometry = get_odometry

        self.fl = PhotonCamera("flCamera")
        self.fr = PhotonCamera("frCamera")
        self.bl = PhotonCamera("blCamera")
        self.br = PhotonCamera("brCamera")

        self.flEstimator = PhotonPoseEstimator(
            AprilTagField(),
            PoseStrategy.MULTI_TAG_PNP_ON_COPROCESSOR,
            self.fl,
            Transform3d(
                inchesToMeters(10.5),
                inchesToMeters(10.5),
                inchesToMeters(8.0),
                Rotation3d(0, 0, degreesToRadians(45)),
            ),
        )
        self.frEstimator = PhotonPoseEstimator(
            AprilTagField(),
            PoseStrategy.MULTI_TAG_PNP_ON_COPROCESSOR,
            self.fr,
            Transform3d(
                inchesToMeters(10.5),
                inchesToMeters(-10.5),
                inchesToMeters(8.0),
                Rotation3d(0, 0, degreesToRadians(-45)),
            ),
        )
        self.blEstimator = PhotonPoseEstimator(
            AprilTagField(),
            PoseStrategy.MULTI_TAG_PNP_ON_COPROCESSOR,
            self.bl,
            Transform3d(
                inchesToMeters(-10.5),
                inchesToMeters(10.5),
                inchesToMeters(8.0),
                Rotation3d(0, 0, degreesToRadians(135)),
            ),
        )
        self.brEstimator = PhotonPoseEstimator(
            AprilTagField(),
            PoseStrategy.MULTI_TAG_PNP_ON_COPROCESSOR,
            self.br,
            Transform3d(
                inchesToMeters(-10.5),
                inchesToMeters(-10.5),
                inchesToMeters(8.0),
                Rotation3d(0, 0, degreesToRadians(-135)),
            ),
        )

    def periodic(self) -> None:
        self.get_odometry().addVisionMeasurement(
            self.flEstimator.update(self.fl.getLatestResult()).estimatedPose.toPose2d()
        )
        self.get_odometry().addVisionMeasurement(
            self.frEstimator.update(self.fr.getLatestResult()).estimatedPose.toPose2d()
        )
        self.get_odometry().addVisionMeasurement(
            self.blEstimator.update(self.bl.getLatestResult()).estimatedPose.toPose2d()
        )
        self.get_odometry().addVisionMeasurement(
            self.brEstimator.update(self.br.getLatestResult()).estimatedPose.toPose2d()
        )
