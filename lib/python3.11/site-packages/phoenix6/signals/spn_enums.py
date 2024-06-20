"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from enum import Enum


class System_StateValue(Enum):
    """
    System state of the device
    """
    BOOTUP_0 = 0
    BOOTUP_1 = 1
    BOOTUP_2 = 2
    BOOTUP_3 = 3
    BOOTUP_4 = 4
    BOOTUP_5 = 5
    BOOTUP_6 = 6
    BOOTUP_7 = 7
    BOOT_BEEP = 8
    CONTROL_DISABLED = 9
    CONTROL_ENABLED = 10
    CONTROL_ENABLED_11 = 11
    FAULT = 12
    RECOVER = 13
    NOT_LICENSED = 14
    PRODUCTION = 15


class IsPROLicensedValue(Enum):
    """
    Whether the device is Pro licensed
    """
    NOT_LICENSED = 0
    LICENSED = 1


class Licensing_IsSeasonPassedValue(Enum):
    """
    Whether the device is Season Pass licensed
    """
    NOT_LICENSED = 0
    LICENSED = 1


class SensorDirectionValue(Enum):
    """
    Direction of the sensor to determine positive rotation, as seen facing the LED
    side of the CANcoder.
    """
    COUNTER_CLOCKWISE_POSITIVE = 0
    CLOCKWISE_POSITIVE = 1


class FrcLockValue(Enum):
    """
    Whether device is locked by FRC.
    """
    FRC_LOCKED = 1
    FRC_UNLOCKED = 0


class RobotEnableValue(Enum):
    """
    Whether the robot is enabled.
    """
    ENABLED = 1
    DISABLED = 0


class Led1OnColorValue(Enum):
    """
    The Color of LED1 when it's "On".
    """
    OFF = 0
    RED = 1
    GREEN = 2
    ORANGE = 3
    BLUE = 4
    PINK = 5
    CYAN = 6
    WHITE = 7


class Led1OffColorValue(Enum):
    """
    The Color of LED1 when it's "Off".
    """
    OFF = 0
    RED = 1
    GREEN = 2
    ORANGE = 3
    BLUE = 4
    PINK = 5
    CYAN = 6
    WHITE = 7


class Led2OnColorValue(Enum):
    """
    The Color of LED2 when it's "On".
    """
    OFF = 0
    RED = 1
    GREEN = 2
    ORANGE = 3
    BLUE = 4
    PINK = 5
    CYAN = 6
    WHITE = 7


class Led2OffColorValue(Enum):
    """
    The Color of LED2 when it's "Off".
    """
    OFF = 0
    RED = 1
    GREEN = 2
    ORANGE = 3
    BLUE = 4
    PINK = 5
    CYAN = 6
    WHITE = 7


class AbsoluteSensorRangeValue(Enum):
    """
    The range of the absolute sensor in rotations, either [-0.5, 0.5) or [0, 1).
    """
    UNSIGNED_0_TO1 = 0
    SIGNED_PLUS_MINUS_HALF = 1


class DeviceEnableValue(Enum):
    """
    Whether the device is enabled.
    """
    ENABLED = 1
    DISABLED = 0


class ForwardLimitValue(Enum):
    """
    Forward Limit Pin.
    """
    CLOSED_TO_GROUND = 0
    OPEN = 1


class ReverseLimitValue(Enum):
    """
    Reverse Limit Pin.
    """
    CLOSED_TO_GROUND = 0
    OPEN = 1


class AppliedRotorPolarityValue(Enum):
    """
    The applied rotor polarity.  This typically is determined by the Inverted
    config, but can be overridden if using Follower features.
    """
    POSITIVE_IS_COUNTER_CLOCKWISE = 0
    POSITIVE_IS_CLOCKWISE = 1


class ControlModeValue(Enum):
    """
    The active control mode of the motor controller
    """
    DISABLED_OUTPUT = 0
    NEUTRAL_OUT = 1
    STATIC_BRAKE = 2
    DUTY_CYCLE_OUT = 3
    POSITION_DUTY_CYCLE = 4
    VELOCITY_DUTY_CYCLE = 5
    MOTION_MAGIC_DUTY_CYCLE = 6
    DUTY_CYCLE_FOC = 7
    POSITION_DUTY_CYCLE_FOC = 8
    VELOCITY_DUTY_CYCLE_FOC = 9
    MOTION_MAGIC_DUTY_CYCLE_FOC = 10
    VOLTAGE_OUT = 11
    POSITION_VOLTAGE = 12
    VELOCITY_VOLTAGE = 13
    MOTION_MAGIC_VOLTAGE = 14
    VOLTAGE_FOC = 15
    POSITION_VOLTAGE_FOC = 16
    VELOCITY_VOLTAGE_FOC = 17
    MOTION_MAGIC_VOLTAGE_FOC = 18
    TORQUE_CURRENT_FOC = 19
    POSITION_TORQUE_CURRENT_FOC = 20
    VELOCITY_TORQUE_CURRENT_FOC = 21
    MOTION_MAGIC_TORQUE_CURRENT_FOC = 22
    FOLLOWER = 23
    RESERVED = 24
    COAST_OUT = 25
    UNAUTHORIZED_DEVICE = 26
    MUSIC_TONE = 27
    MOTION_MAGIC_VELOCITY_DUTY_CYCLE = 28
    MOTION_MAGIC_VELOCITY_DUTY_CYCLE_FOC = 29
    MOTION_MAGIC_VELOCITY_VOLTAGE = 30
    MOTION_MAGIC_VELOCITY_VOLTAGE_FOC = 31
    MOTION_MAGIC_VELOCITY_TORQUE_CURRENT_FOC = 32
    MOTION_MAGIC_EXPO_DUTY_CYCLE = 33
    MOTION_MAGIC_EXPO_DUTY_CYCLE_FOC = 34
    MOTION_MAGIC_EXPO_VOLTAGE = 35
    MOTION_MAGIC_EXPO_VOLTAGE_FOC = 36
    MOTION_MAGIC_EXPO_TORQUE_CURRENT_FOC = 37


class MotionMagicIsRunningValue(Enum):
    """
    Check if Motion Magic® is running.  This is equivalent to checking that the
    reported control mode is a Motion Magic® based mode.
    """
    ENABLED = 1
    DISABLED = 0


class DifferentialControlModeValue(Enum):
    """
    The active control mode of the differential controller
    """
    DISABLED_OUTPUT = 0
    NEUTRAL_OUT = 1
    STATIC_BRAKE = 2
    DUTY_CYCLE_OUT = 3
    POSITION_DUTY_CYCLE = 4
    VELOCITY_DUTY_CYCLE = 5
    MOTION_MAGIC_DUTY_CYCLE = 6
    DUTY_CYCLE_FOC = 7
    POSITION_DUTY_CYCLE_FOC = 8
    VELOCITY_DUTY_CYCLE_FOC = 9
    MOTION_MAGIC_DUTY_CYCLE_FOC = 10
    VOLTAGE_OUT = 11
    POSITION_VOLTAGE = 12
    VELOCITY_VOLTAGE = 13
    MOTION_MAGIC_VOLTAGE = 14
    VOLTAGE_FOC = 15
    POSITION_VOLTAGE_FOC = 16
    VELOCITY_VOLTAGE_FOC = 17
    MOTION_MAGIC_VOLTAGE_FOC = 18
    TORQUE_CURRENT_FOC = 19
    POSITION_TORQUE_CURRENT_FOC = 20
    VELOCITY_TORQUE_CURRENT_FOC = 21
    MOTION_MAGIC_TORQUE_CURRENT_FOC = 22
    FOLLOWER = 23
    RESERVED = 24
    COAST_OUT = 25


class GravityTypeValue(Enum):
    """
    Gravity Feedforward/Feedback Type
    
    This determines the type of the gravity feedforward/feedback.
    
    Choose Elevator_Static for systems where the gravity feedforward is constant,
    such as an elevator. The gravity feedforward output will always have the same
    sign.
    
    Choose Arm_Cosine for systems where the gravity feedback is dependent on the
    angular position of the mechanism, such as an arm. The gravity feedback output
    will vary depending on the mechanism angular position. Note that the sensor
    offset and ratios must be configured so that the sensor reports a position of 0
    when the mechanism is horizonal (parallel to the ground), and the reported
    sensor position is 1:1 with the mechanism.
    """
    ELEVATOR_STATIC = 0
    ARM_COSINE = 1


class InvertedValue(Enum):
    """
    Invert state of the device.
    """
    COUNTER_CLOCKWISE_POSITIVE = 0
    CLOCKWISE_POSITIVE = 1


class NeutralModeValue(Enum):
    """
    The state of the motor controller bridge when output is neutral or disabled.
    """
    COAST = 0
    BRAKE = 1


class FeedbackSensorSourceValue(Enum):
    """
    Choose what sensor source is reported via API and used by closed-loop and limit
    features.  The default is RotorSensor, which uses the internal rotor sensor in
    the Talon FX.
    
    Choose RemoteCANcoder to use another CANcoder on the same CAN bus (this also
    requires setting FeedbackRemoteSensorID).  Talon FX will update its position and
    velocity whenever CANcoder publishes its information on CAN bus.
    
    Choose FusedCANcoder (requires Phoenix Pro) and Talon FX will fuse another
    CANcoder's information with the internal rotor, which provides the best possible
    position and velocity for accuracy and bandwidth (this also requires setting
    FeedbackRemoteSensorID).  FusedCANcoder was developed for applications such as
    swerve-azimuth.
    
    Choose SyncCANcoder (requires Phoenix Pro) and Talon FX will synchronize its
    internal rotor position against another CANcoder, then continue to use the rotor
    sensor for closed loop control (this also requires setting
    FeedbackRemoteSensorID).  The TalonFX will report if its internal position
    differs significantly from the reported CANcoder position.  SyncCANcoder was
    developed for mechanisms where there is a risk of the CANcoder failing in such a
    way that it reports a position that does not match the mechanism, such as the
    sensor mounting assembly breaking off.
    
    Choose RemotePigeon2_Yaw, RemotePigeon2_Pitch, and RemotePigeon2_Roll to use
    another Pigeon2 on the same CAN bus (this also requires setting
    FeedbackRemoteSensorID).  Talon FX will update its position to match the
    selected value whenever Pigeon2 publishes its information on CAN bus. Note that
    the Talon FX position will be in rotations and not degrees.
    
    Note: When the feedback source is changed to FusedCANcoder, the Talon FX needs a
    period of time to fuse before sensor-based (soft-limit, closed loop, etc.)
    features are used. This period of time is determined by the update frequency of
    the CANcoder's Position signal.
    """
    ROTOR_SENSOR = 0
    REMOTE_CANCODER = 1
    REMOTE_PIGEON2_YAW = 2
    REMOTE_PIGEON2_PITCH = 3
    REMOTE_PIGEON2_ROLL = 4
    FUSED_CANCODER = 5
    SYNC_CANCODER = 6


class ForwardLimitTypeValue(Enum):
    """
    Determines if the forward limit switch is normally-open (default) or
    normally-closed.
    """
    NORMALLY_OPEN = 0
    NORMALLY_CLOSED = 1


class ForwardLimitSourceValue(Enum):
    """
    Determines where to poll the forward limit switch.  This defaults to the forward
    limit switch pin on the limit switch connector.
    
    Choose RemoteTalonFX to use the forward limit switch attached to another Talon
    FX on the same CAN bus (this also requires setting ForwardLimitRemoteSensorID).
    
    Choose RemoteCANifier to use the forward limit switch attached to another
    CANifier on the same CAN bus (this also requires setting
    ForwardLimitRemoteSensorID).
    
    Choose RemoteCANcoder to use another CANcoder on the same CAN bus (this also
    requires setting ForwardLimitRemoteSensorID).  The forward limit will assert
    when the CANcoder magnet strength changes from BAD (red) to ADEQUATE (orange) or
    GOOD (green).
    """
    LIMIT_SWITCH_PIN = 0
    REMOTE_TALON_FX = 1
    REMOTE_CANIFIER = 2
    REMOTE_CANCODER = 4
    DISABLED = 3


class ReverseLimitTypeValue(Enum):
    """
    Determines if the reverse limit switch is normally-open (default) or
    normally-closed.
    """
    NORMALLY_OPEN = 0
    NORMALLY_CLOSED = 1


class ReverseLimitSourceValue(Enum):
    """
    Determines where to poll the reverse limit switch.  This defaults to the reverse
    limit switch pin on the limit switch connector.
    
    Choose RemoteTalonFX to use the reverse limit switch attached to another Talon
    FX on the same CAN bus (this also requires setting ReverseLimitRemoteSensorID).
    
    Choose RemoteCANifier to use the reverse limit switch attached to another
    CANifier on the same CAN bus (this also requires setting
    ReverseLimitRemoteSensorID).
    
    Choose RemoteCANcoder to use another CANcoder on the same CAN bus (this also
    requires setting ReverseLimitRemoteSensorID).  The reverse limit will assert
    when the CANcoder magnet strength changes from BAD (red) to ADEQUATE (orange) or
    GOOD (green).
    """
    LIMIT_SWITCH_PIN = 0
    REMOTE_TALON_FX = 1
    REMOTE_CANIFIER = 2
    REMOTE_CANCODER = 4
    DISABLED = 3


class MagnetHealthValue(Enum):
    """
    Magnet health as measured by CANcoder.
    
    Magnet health as measured by CANcoder. Red indicates too close or too far,
    Orange is adequate but with reduced accuracy, green is ideal. Invalid means the
    accuracy cannot be determined.
    """
    MAGNET_RED = 1
    MAGNET_ORANGE = 2
    MAGNET_GREEN = 3
    MAGNET_INVALID = 0


class BridgeOutputValue(Enum):
    """
    The applied output of the bridge.
    """
    BRIDGE_REQ_COAST = 0
    BRIDGE_REQ_BRAKE = 1
    BRIDGE_REQ_TRAPEZ = 6
    BRIDGE_REQ_FOCTORQUE = 7
    BRIDGE_REQ_MUSIC_TONE = 8
    BRIDGE_REQ_FOCEASY = 9
    BRIDGE_REQ_FAULT_BRAKE = 12
    BRIDGE_REQ_FAULT_COAST = 13
    BRIDGE_REQ_ACTIVE_BRAKE = 14


class DifferentialSensorSourceValue(Enum):
    """
    Choose what sensor source is used for differential control of a mechanism.  The
    default is Disabled.  All other options require setting the
    DifferentialTalonFXSensorID, as the average of this Talon FX's sensor and the
    remote TalonFX's sensor is used for the differential controller's primary
    targets.
    
    Choose RemoteTalonFX_Diff to use another TalonFX on the same CAN bus.  Talon FX
    will update its differential position and velocity whenever the remote TalonFX
    publishes its information on CAN bus.  The differential controller will use the
    difference between this TalonFX's sensor and the remote Talon FX's sensor for
    the differential component of the output.
    
    Choose RemotePigeon2_Yaw, RemotePigeon2_Pitch, and RemotePigeon2_Roll to use
    another Pigeon2 on the same CAN bus (this also requires setting
    DifferentialRemoteSensorID).  Talon FX will update its differential position to
    match the selected value whenever Pigeon2 publishes its information on CAN bus.
    Note that the Talon FX differential position will be in rotations and not
    degrees.
    
    Choose RemoteCANcoder to use another CANcoder on the same CAN bus (this also
    requires setting DifferentialRemoteSensorID).  Talon FX will update its
    differential position and velocity to match the CANcoder whenever CANcoder
    publishes its information on CAN bus.
    """
    DISABLED = 0
    REMOTE_TALON_FX_DIFF = 1
    REMOTE_PIGEON2_YAW = 2
    REMOTE_PIGEON2_PITCH = 3
    REMOTE_PIGEON2_ROLL = 4
    REMOTE_CANCODER = 5


class StaticFeedforwardSignValue(Enum):
    """
    Static Feedforward Sign during position closed loop
    
    This determines the sign of the applied kS during position closed-loop modes.
    The default behavior uses the velocity reference sign. This works well with
    velocity closed loop, Motion Magic® controls, and position closed loop when
    velocity reference is specified (motion profiling).
    
    However, when using position closed loop with zero velocity reference (no motion
    profiling), the application may want to apply static feedforward based on the
    closed loop error sign instead. When doing so, we recommend the minimal amount
    of kS, otherwise the motor output may dither when closed loop error is near
    zero.
    """
    USE_VELOCITY_SIGN = 0
    USE_CLOSED_LOOP_SIGN = 1


class MotorTypeValue(Enum):
    """
    The type of motor attached to the Talon FX
    
    This can be used to determine what motor is attached to the Talon FX.  Return
    will be "Unknown" if firmware is too old or device is not present.
    """
    UNKNOWN = 0
    FALCON500 = 1
    KRAKENX60 = 2


class MotorOutputStatusValue(Enum):
    """
    Assess the status of the motor output with respect to load and supply.
    
    This routine can be used to determine the general status of motor commutation. 
    Off means that motor output is disabled.  StaticBraking typically means the
    motor is in neutral-brake.  Motoring means motor is loaded in a typical fashion,
    drawing current from the supply, and successfully turning the rotor in the
    direction of applied voltage.  Discordant Motoring is the same as Motoring,
    expect the rotor is being backdriven as the motor output is not enough to defeat
    load forces.  RegenBraking means the motor is braking in such a way where motor
    current is traveling back to the supply (typically a battery).
    """
    UNKNOWN = 0
    OFF = 1
    STATIC_BRAKING = 2
    MOTORING = 3
    DISCORDANT_MOTORING = 4
    REGEN_BRAKING = 5

