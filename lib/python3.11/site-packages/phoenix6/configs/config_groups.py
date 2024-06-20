"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.status_code import StatusCode
from phoenix6.phoenix_native import Native
from phoenix6.spns.spn_value import SpnValue
from phoenix6.signals.spn_enums import *
from typing import Protocol
import ctypes

class SupportsSerialization(Protocol):
    def serialize(self) -> str:
        pass
    def deserialize(self, string: str) -> StatusCode:
        pass


class MagnetSensorConfigs:
    """
    Configs that affect the magnet sensor and how to interpret it.
    
    Includes sensor range, sensor direction, and the magnet offset.
    """

    def __init__(self):
        self.sensor_direction: SensorDirectionValue = SensorDirectionValue.COUNTER_CLOCKWISE_POSITIVE
        """
        Direction of the sensor to determine positive rotation, as seen facing
        the LED side of the CANcoder.
        
        """
        self.magnet_offset: float = 0
        """
        This offset is added to the reported position, allowing the
        application to trim the zero position.  When set to the default value
        of zero, position reports zero when magnet north pole aligns with the
        LED.
        
            - Minimum Value: -1
            - Maximum Value: 1
            - Default Value: 0
            - Units: rotations
        """
        self.absolute_sensor_range: AbsoluteSensorRangeValue = AbsoluteSensorRangeValue.SIGNED_PLUS_MINUS_HALF
        """
        The range of the absolute sensor in rotations, either [-0.5, 0.5) or
        [0, 1).
        
        """
    
    def with_sensor_direction(self, new_sensor_direction: SensorDirectionValue) -> 'MagnetSensorConfigs':
        """
        Modifies this configuration's sensor_direction parameter and returns itself for
        method-chaining and easier to use config API.
    
        Direction of the sensor to determine positive rotation, as seen facing
        the LED side of the CANcoder.
        
    
        :param new_sensor_direction: Parameter to modify
        :type new_sensor_direction: SensorDirectionValue
        :returns: Itself
        :rtype: MagnetSensorConfigs
        """
        self.sensor_direction = new_sensor_direction
        return self
    
    def with_magnet_offset(self, new_magnet_offset: float) -> 'MagnetSensorConfigs':
        """
        Modifies this configuration's magnet_offset parameter and returns itself for
        method-chaining and easier to use config API.
    
        This offset is added to the reported position, allowing the
        application to trim the zero position.  When set to the default value
        of zero, position reports zero when magnet north pole aligns with the
        LED.
        
            - Minimum Value: -1
            - Maximum Value: 1
            - Default Value: 0
            - Units: rotations
    
        :param new_magnet_offset: Parameter to modify
        :type new_magnet_offset: float
        :returns: Itself
        :rtype: MagnetSensorConfigs
        """
        self.magnet_offset = new_magnet_offset
        return self
    
    def with_absolute_sensor_range(self, new_absolute_sensor_range: AbsoluteSensorRangeValue) -> 'MagnetSensorConfigs':
        """
        Modifies this configuration's absolute_sensor_range parameter and returns itself for
        method-chaining and easier to use config API.
    
        The range of the absolute sensor in rotations, either [-0.5, 0.5) or
        [0, 1).
        
    
        :param new_absolute_sensor_range: Parameter to modify
        :type new_absolute_sensor_range: AbsoluteSensorRangeValue
        :returns: Itself
        :rtype: MagnetSensorConfigs
        """
        self.absolute_sensor_range = new_absolute_sensor_range
        return self
    


    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: MagnetSensor")
        ss.append("Name: \"SensorDirection\" Value: \"" + str(self.sensor_direction) + "\"")
        ss.append("Name: \"MagnetOffset\" Value: \"" + str(self.magnet_offset) + "rotations\"")
        ss.append("Name: \"AbsoluteSensorRange\" Value: \"" + str(self.absolute_sensor_range) + "\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.CANCODER_SENSOR_DIRECTION.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.sensor_direction = SensorDirectionValue(value.value)
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CANCODER_MAGNET_OFFSET.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.magnet_offset = value.value
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.CANCODER_ABSOLUTE_SENSOR_RANGE.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.absolute_sensor_range = AbsoluteSensorRangeValue(value.value)
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.CANCODER_SENSOR_DIRECTION.value, self.sensor_direction.value, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CANCODER_MAGNET_OFFSET.value, self.magnet_offset, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.CANCODER_ABSOLUTE_SENSOR_RANGE.value, self.absolute_sensor_range.value, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)


class MountPoseConfigs:
    """
    Configs for Pigeon 2's Mount Pose configuration.
    
    These configs allow the Pigeon2 to be mounted in whatever orientation
    that's desired and ensure the reported Yaw/Pitch/Roll is from the
    robot's reference.
    """

    def __init__(self):
        self.mount_pose_yaw: float = 0
        """
        The mounting calibration yaw-component
        
            - Minimum Value: -360
            - Maximum Value: 360
            - Default Value: 0
            - Units: deg
        """
        self.mount_pose_pitch: float = 0
        """
        The mounting calibration pitch-component
        
            - Minimum Value: -360
            - Maximum Value: 360
            - Default Value: 0
            - Units: deg
        """
        self.mount_pose_roll: float = 0
        """
        The mounting calibration roll-component
        
            - Minimum Value: -360
            - Maximum Value: 360
            - Default Value: 0
            - Units: deg
        """
    
    def with_mount_pose_yaw(self, new_mount_pose_yaw: float) -> 'MountPoseConfigs':
        """
        Modifies this configuration's mount_pose_yaw parameter and returns itself for
        method-chaining and easier to use config API.
    
        The mounting calibration yaw-component
        
            - Minimum Value: -360
            - Maximum Value: 360
            - Default Value: 0
            - Units: deg
    
        :param new_mount_pose_yaw: Parameter to modify
        :type new_mount_pose_yaw: float
        :returns: Itself
        :rtype: MountPoseConfigs
        """
        self.mount_pose_yaw = new_mount_pose_yaw
        return self
    
    def with_mount_pose_pitch(self, new_mount_pose_pitch: float) -> 'MountPoseConfigs':
        """
        Modifies this configuration's mount_pose_pitch parameter and returns itself for
        method-chaining and easier to use config API.
    
        The mounting calibration pitch-component
        
            - Minimum Value: -360
            - Maximum Value: 360
            - Default Value: 0
            - Units: deg
    
        :param new_mount_pose_pitch: Parameter to modify
        :type new_mount_pose_pitch: float
        :returns: Itself
        :rtype: MountPoseConfigs
        """
        self.mount_pose_pitch = new_mount_pose_pitch
        return self
    
    def with_mount_pose_roll(self, new_mount_pose_roll: float) -> 'MountPoseConfigs':
        """
        Modifies this configuration's mount_pose_roll parameter and returns itself for
        method-chaining and easier to use config API.
    
        The mounting calibration roll-component
        
            - Minimum Value: -360
            - Maximum Value: 360
            - Default Value: 0
            - Units: deg
    
        :param new_mount_pose_roll: Parameter to modify
        :type new_mount_pose_roll: float
        :returns: Itself
        :rtype: MountPoseConfigs
        """
        self.mount_pose_roll = new_mount_pose_roll
        return self
    


    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: MountPose")
        ss.append("Name: \"MountPoseYaw\" Value: \"" + str(self.mount_pose_yaw) + "deg\"")
        ss.append("Name: \"MountPosePitch\" Value: \"" + str(self.mount_pose_pitch) + "deg\"")
        ss.append("Name: \"MountPoseRoll\" Value: \"" + str(self.mount_pose_roll) + "deg\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.PIGEON2_MOUNT_POSE_YAW.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.mount_pose_yaw = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.PIGEON2_MOUNT_POSE_PITCH.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.mount_pose_pitch = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.PIGEON2_MOUNT_POSE_ROLL.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.mount_pose_roll = value.value
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.PIGEON2_MOUNT_POSE_YAW.value, self.mount_pose_yaw, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.PIGEON2_MOUNT_POSE_PITCH.value, self.mount_pose_pitch, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.PIGEON2_MOUNT_POSE_ROLL.value, self.mount_pose_roll, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)


class GyroTrimConfigs:
    """
    Configs to trim the Pigeon2's gyroscope.
    
    Pigeon2 allows the user to trim the gyroscope's sensitivity. While
    this isn't necessary for the Pigeon2, as it comes calibrated
    out-of-the-box, users can make use of this to make the Pigeon2 even
    more accurate for their application.
    """

    def __init__(self):
        self.gyro_scalar_x: float = 0
        """
        The gyro scalar component for the X axis
        
            - Minimum Value: -180
            - Maximum Value: 180
            - Default Value: 0
            - Units: deg per rotation
        """
        self.gyro_scalar_y: float = 0
        """
        The gyro scalar component for the Y axis
        
            - Minimum Value: -180
            - Maximum Value: 180
            - Default Value: 0
            - Units: deg per rotation
        """
        self.gyro_scalar_z: float = 0
        """
        The gyro scalar component for the Z axis
        
            - Minimum Value: -180
            - Maximum Value: 180
            - Default Value: 0
            - Units: deg per rotation
        """
    
    def with_gyro_scalar_x(self, new_gyro_scalar_x: float) -> 'GyroTrimConfigs':
        """
        Modifies this configuration's gyro_scalar_x parameter and returns itself for
        method-chaining and easier to use config API.
    
        The gyro scalar component for the X axis
        
            - Minimum Value: -180
            - Maximum Value: 180
            - Default Value: 0
            - Units: deg per rotation
    
        :param new_gyro_scalar_x: Parameter to modify
        :type new_gyro_scalar_x: float
        :returns: Itself
        :rtype: GyroTrimConfigs
        """
        self.gyro_scalar_x = new_gyro_scalar_x
        return self
    
    def with_gyro_scalar_y(self, new_gyro_scalar_y: float) -> 'GyroTrimConfigs':
        """
        Modifies this configuration's gyro_scalar_y parameter and returns itself for
        method-chaining and easier to use config API.
    
        The gyro scalar component for the Y axis
        
            - Minimum Value: -180
            - Maximum Value: 180
            - Default Value: 0
            - Units: deg per rotation
    
        :param new_gyro_scalar_y: Parameter to modify
        :type new_gyro_scalar_y: float
        :returns: Itself
        :rtype: GyroTrimConfigs
        """
        self.gyro_scalar_y = new_gyro_scalar_y
        return self
    
    def with_gyro_scalar_z(self, new_gyro_scalar_z: float) -> 'GyroTrimConfigs':
        """
        Modifies this configuration's gyro_scalar_z parameter and returns itself for
        method-chaining and easier to use config API.
    
        The gyro scalar component for the Z axis
        
            - Minimum Value: -180
            - Maximum Value: 180
            - Default Value: 0
            - Units: deg per rotation
    
        :param new_gyro_scalar_z: Parameter to modify
        :type new_gyro_scalar_z: float
        :returns: Itself
        :rtype: GyroTrimConfigs
        """
        self.gyro_scalar_z = new_gyro_scalar_z
        return self
    


    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: GyroTrim")
        ss.append("Name: \"GyroScalarX\" Value: \"" + str(self.gyro_scalar_x) + "deg per rotation\"")
        ss.append("Name: \"GyroScalarY\" Value: \"" + str(self.gyro_scalar_y) + "deg per rotation\"")
        ss.append("Name: \"GyroScalarZ\" Value: \"" + str(self.gyro_scalar_z) + "deg per rotation\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.PIGEON2_GYRO_SCALARX.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.gyro_scalar_x = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.PIGEON2_GYRO_SCALARY.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.gyro_scalar_y = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.PIGEON2_GYRO_SCALARZ.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.gyro_scalar_z = value.value
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.PIGEON2_GYRO_SCALARX.value, self.gyro_scalar_x, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.PIGEON2_GYRO_SCALARY.value, self.gyro_scalar_y, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.PIGEON2_GYRO_SCALARZ.value, self.gyro_scalar_z, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)


class Pigeon2FeaturesConfigs:
    """
    Configs to enable/disable various features of the Pigeon2.
    
    These configs allow the user to enable or disable various aspects of
    the Pigeon2.
    """

    def __init__(self):
        self.enable_compass: bool = False
        """
        Turns on or off the magnetometer fusing for 9-axis. FRC users are not
        recommended to turn this on, as the magnetic influence of the robot
        will likely negatively affect the performance of the Pigeon2.
        
            - Default Value: False
        """
        self.disable_temperature_compensation: bool = False
        """
        Disables using the temperature compensation feature
        
            - Default Value: False
        """
        self.disable_no_motion_calibration: bool = False
        """
        Disables using the no-motion calibration feature
        
            - Default Value: False
        """
    
    def with_enable_compass(self, new_enable_compass: bool) -> 'Pigeon2FeaturesConfigs':
        """
        Modifies this configuration's enable_compass parameter and returns itself for
        method-chaining and easier to use config API.
    
        Turns on or off the magnetometer fusing for 9-axis. FRC users are not
        recommended to turn this on, as the magnetic influence of the robot
        will likely negatively affect the performance of the Pigeon2.
        
            - Default Value: False
    
        :param new_enable_compass: Parameter to modify
        :type new_enable_compass: bool
        :returns: Itself
        :rtype: Pigeon2FeaturesConfigs
        """
        self.enable_compass = new_enable_compass
        return self
    
    def with_disable_temperature_compensation(self, new_disable_temperature_compensation: bool) -> 'Pigeon2FeaturesConfigs':
        """
        Modifies this configuration's disable_temperature_compensation parameter and returns itself for
        method-chaining and easier to use config API.
    
        Disables using the temperature compensation feature
        
            - Default Value: False
    
        :param new_disable_temperature_compensation: Parameter to modify
        :type new_disable_temperature_compensation: bool
        :returns: Itself
        :rtype: Pigeon2FeaturesConfigs
        """
        self.disable_temperature_compensation = new_disable_temperature_compensation
        return self
    
    def with_disable_no_motion_calibration(self, new_disable_no_motion_calibration: bool) -> 'Pigeon2FeaturesConfigs':
        """
        Modifies this configuration's disable_no_motion_calibration parameter and returns itself for
        method-chaining and easier to use config API.
    
        Disables using the no-motion calibration feature
        
            - Default Value: False
    
        :param new_disable_no_motion_calibration: Parameter to modify
        :type new_disable_no_motion_calibration: bool
        :returns: Itself
        :rtype: Pigeon2FeaturesConfigs
        """
        self.disable_no_motion_calibration = new_disable_no_motion_calibration
        return self
    


    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: Pigeon2Features")
        ss.append("Name: \"EnableCompass\" Value: \"" + str(self.enable_compass) + "\"")
        ss.append("Name: \"DisableTemperatureCompensation\" Value: \"" + str(self.disable_temperature_compensation) + "\"")
        ss.append("Name: \"DisableNoMotionCalibration\" Value: \"" + str(self.disable_no_motion_calibration) + "\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_bool()
        Native.instance().c_ctre_phoenix6_deserialize_bool(SpnValue.PIGEON2_USE_COMPASS.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.enable_compass = value.value
        value = ctypes.c_bool()
        Native.instance().c_ctre_phoenix6_deserialize_bool(SpnValue.PIGEON2_DISABLE_TEMPERATURE_COMPENSATION.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.disable_temperature_compensation = value.value
        value = ctypes.c_bool()
        Native.instance().c_ctre_phoenix6_deserialize_bool(SpnValue.PIGEON2_DISABLE_NO_MOTION_CALIBRATION.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.disable_no_motion_calibration = value.value
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_bool(SpnValue.PIGEON2_USE_COMPASS.value, self.enable_compass, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_bool(SpnValue.PIGEON2_DISABLE_TEMPERATURE_COMPENSATION.value, self.disable_temperature_compensation, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_bool(SpnValue.PIGEON2_DISABLE_NO_MOTION_CALIBRATION.value, self.disable_no_motion_calibration, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)


class MotorOutputConfigs:
    """
    Configs that directly affect motor output.
    
    Includes motor invert, neutral mode, and other features related to
    motor output.
    """

    def __init__(self):
        self.inverted: InvertedValue = InvertedValue.COUNTER_CLOCKWISE_POSITIVE
        """
        Invert state of the device.
        
        """
        self.neutral_mode: NeutralModeValue = NeutralModeValue.COAST
        """
        The state of the motor controller bridge when output is neutral or
        disabled.
        
        """
        self.duty_cycle_neutral_deadband: float = 0
        """
        Configures the output deadband duty cycle during duty cycle and
        voltage based control modes.
        
            - Minimum Value: 0.0
            - Maximum Value: 0.25
            - Default Value: 0
            - Units: fractional
        """
        self.peak_forward_duty_cycle: float = 1
        """
        Maximum (forward) output during duty cycle based control modes.
        
            - Minimum Value: -1.0
            - Maximum Value: 1.0
            - Default Value: 1
            - Units: fractional
        """
        self.peak_reverse_duty_cycle: float = -1
        """
        Minimum (reverse) output during duty cycle based control modes.
        
            - Minimum Value: -1.0
            - Maximum Value: 1.0
            - Default Value: -1
            - Units: fractional
        """
    
    def with_inverted(self, new_inverted: InvertedValue) -> 'MotorOutputConfigs':
        """
        Modifies this configuration's inverted parameter and returns itself for
        method-chaining and easier to use config API.
    
        Invert state of the device.
        
    
        :param new_inverted: Parameter to modify
        :type new_inverted: InvertedValue
        :returns: Itself
        :rtype: MotorOutputConfigs
        """
        self.inverted = new_inverted
        return self
    
    def with_neutral_mode(self, new_neutral_mode: NeutralModeValue) -> 'MotorOutputConfigs':
        """
        Modifies this configuration's neutral_mode parameter and returns itself for
        method-chaining and easier to use config API.
    
        The state of the motor controller bridge when output is neutral or
        disabled.
        
    
        :param new_neutral_mode: Parameter to modify
        :type new_neutral_mode: NeutralModeValue
        :returns: Itself
        :rtype: MotorOutputConfigs
        """
        self.neutral_mode = new_neutral_mode
        return self
    
    def with_duty_cycle_neutral_deadband(self, new_duty_cycle_neutral_deadband: float) -> 'MotorOutputConfigs':
        """
        Modifies this configuration's duty_cycle_neutral_deadband parameter and returns itself for
        method-chaining and easier to use config API.
    
        Configures the output deadband duty cycle during duty cycle and
        voltage based control modes.
        
            - Minimum Value: 0.0
            - Maximum Value: 0.25
            - Default Value: 0
            - Units: fractional
    
        :param new_duty_cycle_neutral_deadband: Parameter to modify
        :type new_duty_cycle_neutral_deadband: float
        :returns: Itself
        :rtype: MotorOutputConfigs
        """
        self.duty_cycle_neutral_deadband = new_duty_cycle_neutral_deadband
        return self
    
    def with_peak_forward_duty_cycle(self, new_peak_forward_duty_cycle: float) -> 'MotorOutputConfigs':
        """
        Modifies this configuration's peak_forward_duty_cycle parameter and returns itself for
        method-chaining and easier to use config API.
    
        Maximum (forward) output during duty cycle based control modes.
        
            - Minimum Value: -1.0
            - Maximum Value: 1.0
            - Default Value: 1
            - Units: fractional
    
        :param new_peak_forward_duty_cycle: Parameter to modify
        :type new_peak_forward_duty_cycle: float
        :returns: Itself
        :rtype: MotorOutputConfigs
        """
        self.peak_forward_duty_cycle = new_peak_forward_duty_cycle
        return self
    
    def with_peak_reverse_duty_cycle(self, new_peak_reverse_duty_cycle: float) -> 'MotorOutputConfigs':
        """
        Modifies this configuration's peak_reverse_duty_cycle parameter and returns itself for
        method-chaining and easier to use config API.
    
        Minimum (reverse) output during duty cycle based control modes.
        
            - Minimum Value: -1.0
            - Maximum Value: 1.0
            - Default Value: -1
            - Units: fractional
    
        :param new_peak_reverse_duty_cycle: Parameter to modify
        :type new_peak_reverse_duty_cycle: float
        :returns: Itself
        :rtype: MotorOutputConfigs
        """
        self.peak_reverse_duty_cycle = new_peak_reverse_duty_cycle
        return self
    


    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: MotorOutput")
        ss.append("Name: \"Inverted\" Value: \"" + str(self.inverted) + "\"")
        ss.append("Name: \"NeutralMode\" Value: \"" + str(self.neutral_mode) + "\"")
        ss.append("Name: \"DutyCycleNeutralDeadband\" Value: \"" + str(self.duty_cycle_neutral_deadband) + "fractional\"")
        ss.append("Name: \"PeakForwardDutyCycle\" Value: \"" + str(self.peak_forward_duty_cycle) + "fractional\"")
        ss.append("Name: \"PeakReverseDutyCycle\" Value: \"" + str(self.peak_reverse_duty_cycle) + "fractional\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.CONFIG_INVERTED.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.inverted = InvertedValue(value.value)
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.CONFIG_NEUTRAL_MODE.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.neutral_mode = NeutralModeValue(value.value)
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_DUTY_CYCLE_NEUTRAL_DB.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.duty_cycle_neutral_deadband = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_PEAK_FORWARD_DC.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.peak_forward_duty_cycle = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_PEAK_REVERSE_DC.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.peak_reverse_duty_cycle = value.value
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.CONFIG_INVERTED.value, self.inverted.value, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.CONFIG_NEUTRAL_MODE.value, self.neutral_mode.value, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_DUTY_CYCLE_NEUTRAL_DB.value, self.duty_cycle_neutral_deadband, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_PEAK_FORWARD_DC.value, self.peak_forward_duty_cycle, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_PEAK_REVERSE_DC.value, self.peak_reverse_duty_cycle, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)


class CurrentLimitsConfigs:
    """
    Configs that directly affect current limiting features.
    
    Contains the supply/stator current limit thresholds and whether to
    enable them.
    """

    def __init__(self):
        self.stator_current_limit: float = 0
        """
        The amount of current allowed in the motor (motoring and regen
        current).  Note this requires StatorCurrentLimitEnable to be true.
        
        This is only applicable for non-torque current control modes.  For
        torque current control, set the PeakForwardTorqueCurrent and
        PeakReverseTorqueCurrent in TorqueCurrentConfigs instead.
        
        Stator current is directly proportional to torque, so this limit can
        be used to restrict the torque output of the motor, such as preventing
        wheel slip for a drivetrain.  Additionally, stator current limits can
        prevent brownouts during acceleration; supply current will never
        exceed the stator current limit and is often significantly lower than
        stator current.
        
        A reasonable starting point for a stator current limit is 120 A, with
        values commonly ranging from 80-160 A. Mechanisms with a hard stop may
        need a smaller limit to reduce the torque applied when running into
        the hard stop.
        
            - Minimum Value: 0.0
            - Maximum Value: 800.0
            - Default Value: 0
            - Units: A
        """
        self.stator_current_limit_enable: bool = False
        """
        Enable motor stator current limiting.
        
            - Default Value: False
        """
        self.supply_current_limit: float = 0
        """
        The amount of supply current allowed.  Note this requires
        SupplyCurrentLimitEnable to be true.  Use SupplyCurrentThreshold and
        SupplyTimeThreshold to allow brief periods of high-current before
        limiting occurs.
        
        This is only applicable for non-torque current control modes.  For
        torque current control, set the PeakForwardTorqueCurrent and
        PeakReverseTorqueCurrent in TorqueCurrentConfigs instead.
        
        Supply current is the current drawn from the battery, so this limit
        can be used to prevent breaker trips and improve battery longevity. 
        Additionally, in the rare case where the robot experiences brownouts
        despite configuring stator current limits, a supply current limit can
        further help avoid brownouts. However, such brownouts are most
        commonly caused by a bad battery or poor power wiring.
        
        A reasonable starting point for a supply current limit is 60 A with a
        threshold of 80 A for 0.1 seconds. Supply current limits commonly
        range from 20-80 A depending on the breaker used.
        
            - Minimum Value: 0.0
            - Maximum Value: 800.0
            - Default Value: 0
            - Units: A
        """
        self.supply_current_limit_enable: bool = False
        """
        Enable motor supply current limiting.
        
            - Default Value: False
        """
        self.supply_current_threshold: float = 0
        """
        Delay supply current limiting until current exceeds this threshold for
        longer than SupplyTimeThreshold.  This allows current draws above
        SupplyCurrentLimit for a fixed period of time.  This has no effect if
        SupplyCurrentLimit is greater than this value.
        
            - Minimum Value: 0.0
            - Maximum Value: 511
            - Default Value: 0
            - Units: A
        """
        self.supply_time_threshold: float = 0
        """
        Allows unlimited current for a period of time before current limiting
        occurs.  Current threshold is the maximum of SupplyCurrentThreshold
        and SupplyCurrentLimit.
        
            - Minimum Value: 0.0
            - Maximum Value: 1.275
            - Default Value: 0
            - Units: sec
        """
    
    def with_stator_current_limit(self, new_stator_current_limit: float) -> 'CurrentLimitsConfigs':
        """
        Modifies this configuration's stator_current_limit parameter and returns itself for
        method-chaining and easier to use config API.
    
        The amount of current allowed in the motor (motoring and regen
        current).  Note this requires StatorCurrentLimitEnable to be true.
        
        This is only applicable for non-torque current control modes.  For
        torque current control, set the PeakForwardTorqueCurrent and
        PeakReverseTorqueCurrent in TorqueCurrentConfigs instead.
        
        Stator current is directly proportional to torque, so this limit can
        be used to restrict the torque output of the motor, such as preventing
        wheel slip for a drivetrain.  Additionally, stator current limits can
        prevent brownouts during acceleration; supply current will never
        exceed the stator current limit and is often significantly lower than
        stator current.
        
        A reasonable starting point for a stator current limit is 120 A, with
        values commonly ranging from 80-160 A. Mechanisms with a hard stop may
        need a smaller limit to reduce the torque applied when running into
        the hard stop.
        
            - Minimum Value: 0.0
            - Maximum Value: 800.0
            - Default Value: 0
            - Units: A
    
        :param new_stator_current_limit: Parameter to modify
        :type new_stator_current_limit: float
        :returns: Itself
        :rtype: CurrentLimitsConfigs
        """
        self.stator_current_limit = new_stator_current_limit
        return self
    
    def with_stator_current_limit_enable(self, new_stator_current_limit_enable: bool) -> 'CurrentLimitsConfigs':
        """
        Modifies this configuration's stator_current_limit_enable parameter and returns itself for
        method-chaining and easier to use config API.
    
        Enable motor stator current limiting.
        
            - Default Value: False
    
        :param new_stator_current_limit_enable: Parameter to modify
        :type new_stator_current_limit_enable: bool
        :returns: Itself
        :rtype: CurrentLimitsConfigs
        """
        self.stator_current_limit_enable = new_stator_current_limit_enable
        return self
    
    def with_supply_current_limit(self, new_supply_current_limit: float) -> 'CurrentLimitsConfigs':
        """
        Modifies this configuration's supply_current_limit parameter and returns itself for
        method-chaining and easier to use config API.
    
        The amount of supply current allowed.  Note this requires
        SupplyCurrentLimitEnable to be true.  Use SupplyCurrentThreshold and
        SupplyTimeThreshold to allow brief periods of high-current before
        limiting occurs.
        
        This is only applicable for non-torque current control modes.  For
        torque current control, set the PeakForwardTorqueCurrent and
        PeakReverseTorqueCurrent in TorqueCurrentConfigs instead.
        
        Supply current is the current drawn from the battery, so this limit
        can be used to prevent breaker trips and improve battery longevity. 
        Additionally, in the rare case where the robot experiences brownouts
        despite configuring stator current limits, a supply current limit can
        further help avoid brownouts. However, such brownouts are most
        commonly caused by a bad battery or poor power wiring.
        
        A reasonable starting point for a supply current limit is 60 A with a
        threshold of 80 A for 0.1 seconds. Supply current limits commonly
        range from 20-80 A depending on the breaker used.
        
            - Minimum Value: 0.0
            - Maximum Value: 800.0
            - Default Value: 0
            - Units: A
    
        :param new_supply_current_limit: Parameter to modify
        :type new_supply_current_limit: float
        :returns: Itself
        :rtype: CurrentLimitsConfigs
        """
        self.supply_current_limit = new_supply_current_limit
        return self
    
    def with_supply_current_limit_enable(self, new_supply_current_limit_enable: bool) -> 'CurrentLimitsConfigs':
        """
        Modifies this configuration's supply_current_limit_enable parameter and returns itself for
        method-chaining and easier to use config API.
    
        Enable motor supply current limiting.
        
            - Default Value: False
    
        :param new_supply_current_limit_enable: Parameter to modify
        :type new_supply_current_limit_enable: bool
        :returns: Itself
        :rtype: CurrentLimitsConfigs
        """
        self.supply_current_limit_enable = new_supply_current_limit_enable
        return self
    
    def with_supply_current_threshold(self, new_supply_current_threshold: float) -> 'CurrentLimitsConfigs':
        """
        Modifies this configuration's supply_current_threshold parameter and returns itself for
        method-chaining and easier to use config API.
    
        Delay supply current limiting until current exceeds this threshold for
        longer than SupplyTimeThreshold.  This allows current draws above
        SupplyCurrentLimit for a fixed period of time.  This has no effect if
        SupplyCurrentLimit is greater than this value.
        
            - Minimum Value: 0.0
            - Maximum Value: 511
            - Default Value: 0
            - Units: A
    
        :param new_supply_current_threshold: Parameter to modify
        :type new_supply_current_threshold: float
        :returns: Itself
        :rtype: CurrentLimitsConfigs
        """
        self.supply_current_threshold = new_supply_current_threshold
        return self
    
    def with_supply_time_threshold(self, new_supply_time_threshold: float) -> 'CurrentLimitsConfigs':
        """
        Modifies this configuration's supply_time_threshold parameter and returns itself for
        method-chaining and easier to use config API.
    
        Allows unlimited current for a period of time before current limiting
        occurs.  Current threshold is the maximum of SupplyCurrentThreshold
        and SupplyCurrentLimit.
        
            - Minimum Value: 0.0
            - Maximum Value: 1.275
            - Default Value: 0
            - Units: sec
    
        :param new_supply_time_threshold: Parameter to modify
        :type new_supply_time_threshold: float
        :returns: Itself
        :rtype: CurrentLimitsConfigs
        """
        self.supply_time_threshold = new_supply_time_threshold
        return self
    


    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: CurrentLimits")
        ss.append("Name: \"StatorCurrentLimit\" Value: \"" + str(self.stator_current_limit) + "A\"")
        ss.append("Name: \"StatorCurrentLimitEnable\" Value: \"" + str(self.stator_current_limit_enable) + "\"")
        ss.append("Name: \"SupplyCurrentLimit\" Value: \"" + str(self.supply_current_limit) + "A\"")
        ss.append("Name: \"SupplyCurrentLimitEnable\" Value: \"" + str(self.supply_current_limit_enable) + "\"")
        ss.append("Name: \"SupplyCurrentThreshold\" Value: \"" + str(self.supply_current_threshold) + "A\"")
        ss.append("Name: \"SupplyTimeThreshold\" Value: \"" + str(self.supply_time_threshold) + "sec\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_STATOR_CURRENT_LIMIT.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.stator_current_limit = value.value
        value = ctypes.c_bool()
        Native.instance().c_ctre_phoenix6_deserialize_bool(SpnValue.CONFIG_STATOR_CURR_LIMIT_EN.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.stator_current_limit_enable = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_SUPPLY_CURRENT_LIMIT.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.supply_current_limit = value.value
        value = ctypes.c_bool()
        Native.instance().c_ctre_phoenix6_deserialize_bool(SpnValue.CONFIG_SUPPLY_CURR_LIMIT_EN.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.supply_current_limit_enable = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_SUPPLY_CURR_THRES.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.supply_current_threshold = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_SUPPLY_TIME_THRES.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.supply_time_threshold = value.value
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_STATOR_CURRENT_LIMIT.value, self.stator_current_limit, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_bool(SpnValue.CONFIG_STATOR_CURR_LIMIT_EN.value, self.stator_current_limit_enable, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_SUPPLY_CURRENT_LIMIT.value, self.supply_current_limit, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_bool(SpnValue.CONFIG_SUPPLY_CURR_LIMIT_EN.value, self.supply_current_limit_enable, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_SUPPLY_CURR_THRES.value, self.supply_current_threshold, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_SUPPLY_TIME_THRES.value, self.supply_time_threshold, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)


class VoltageConfigs:
    """
    Configs that affect Voltage control types.
    
    Includes peak output voltages and other configs affecting voltage
    measurements.
    """

    def __init__(self):
        self.supply_voltage_time_constant: float = 0
        """
        The time constant (in seconds) of the low-pass filter for the supply
        voltage.
        
        This impacts the filtering for the reported supply voltage, and any
        control strategies that use the supply voltage (such as voltage
        control on a motor controller).
        
            - Minimum Value: 0.0
            - Maximum Value: 0.1
            - Default Value: 0
            - Units: sec
        """
        self.peak_forward_voltage: float = 16
        """
        Maximum (forward) output during voltage based control modes.
        
            - Minimum Value: -16
            - Maximum Value: 16
            - Default Value: 16
            - Units: V
        """
        self.peak_reverse_voltage: float = -16
        """
        Minimum (reverse) output during voltage based control modes.
        
            - Minimum Value: -16
            - Maximum Value: 16
            - Default Value: -16
            - Units: V
        """
    
    def with_supply_voltage_time_constant(self, new_supply_voltage_time_constant: float) -> 'VoltageConfigs':
        """
        Modifies this configuration's supply_voltage_time_constant parameter and returns itself for
        method-chaining and easier to use config API.
    
        The time constant (in seconds) of the low-pass filter for the supply
        voltage.
        
        This impacts the filtering for the reported supply voltage, and any
        control strategies that use the supply voltage (such as voltage
        control on a motor controller).
        
            - Minimum Value: 0.0
            - Maximum Value: 0.1
            - Default Value: 0
            - Units: sec
    
        :param new_supply_voltage_time_constant: Parameter to modify
        :type new_supply_voltage_time_constant: float
        :returns: Itself
        :rtype: VoltageConfigs
        """
        self.supply_voltage_time_constant = new_supply_voltage_time_constant
        return self
    
    def with_peak_forward_voltage(self, new_peak_forward_voltage: float) -> 'VoltageConfigs':
        """
        Modifies this configuration's peak_forward_voltage parameter and returns itself for
        method-chaining and easier to use config API.
    
        Maximum (forward) output during voltage based control modes.
        
            - Minimum Value: -16
            - Maximum Value: 16
            - Default Value: 16
            - Units: V
    
        :param new_peak_forward_voltage: Parameter to modify
        :type new_peak_forward_voltage: float
        :returns: Itself
        :rtype: VoltageConfigs
        """
        self.peak_forward_voltage = new_peak_forward_voltage
        return self
    
    def with_peak_reverse_voltage(self, new_peak_reverse_voltage: float) -> 'VoltageConfigs':
        """
        Modifies this configuration's peak_reverse_voltage parameter and returns itself for
        method-chaining and easier to use config API.
    
        Minimum (reverse) output during voltage based control modes.
        
            - Minimum Value: -16
            - Maximum Value: 16
            - Default Value: -16
            - Units: V
    
        :param new_peak_reverse_voltage: Parameter to modify
        :type new_peak_reverse_voltage: float
        :returns: Itself
        :rtype: VoltageConfigs
        """
        self.peak_reverse_voltage = new_peak_reverse_voltage
        return self
    


    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: Voltage")
        ss.append("Name: \"SupplyVoltageTimeConstant\" Value: \"" + str(self.supply_voltage_time_constant) + "sec\"")
        ss.append("Name: \"PeakForwardVoltage\" Value: \"" + str(self.peak_forward_voltage) + "V\"")
        ss.append("Name: \"PeakReverseVoltage\" Value: \"" + str(self.peak_reverse_voltage) + "V\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_SUPPLY_VLOWPASS_TAU.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.supply_voltage_time_constant = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_PEAK_FORWARDV.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.peak_forward_voltage = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_PEAK_REVERSEV.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.peak_reverse_voltage = value.value
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_SUPPLY_VLOWPASS_TAU.value, self.supply_voltage_time_constant, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_PEAK_FORWARDV.value, self.peak_forward_voltage, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_PEAK_REVERSEV.value, self.peak_reverse_voltage, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)


class TorqueCurrentConfigs:
    """
    Configs that affect Torque Current control types.
    
    Includes the maximum and minimum applied torque output and the neutral
    deadband used during TorqueCurrentFOC requests.
    """

    def __init__(self):
        self.peak_forward_torque_current: float = 800
        """
        Maximum (forward) output during torque current based control modes.
        
            - Minimum Value: -800
            - Maximum Value: 800
            - Default Value: 800
            - Units: A
        """
        self.peak_reverse_torque_current: float = -800
        """
        Minimum (reverse) output during torque current based control modes.
        
            - Minimum Value: -800
            - Maximum Value: 800
            - Default Value: -800
            - Units: A
        """
        self.torque_neutral_deadband: float = 0.0
        """
        Configures the output deadband during torque current based control
        modes.
        
            - Minimum Value: 0
            - Maximum Value: 25
            - Default Value: 0.0
            - Units: A
        """
    
    def with_peak_forward_torque_current(self, new_peak_forward_torque_current: float) -> 'TorqueCurrentConfigs':
        """
        Modifies this configuration's peak_forward_torque_current parameter and returns itself for
        method-chaining and easier to use config API.
    
        Maximum (forward) output during torque current based control modes.
        
            - Minimum Value: -800
            - Maximum Value: 800
            - Default Value: 800
            - Units: A
    
        :param new_peak_forward_torque_current: Parameter to modify
        :type new_peak_forward_torque_current: float
        :returns: Itself
        :rtype: TorqueCurrentConfigs
        """
        self.peak_forward_torque_current = new_peak_forward_torque_current
        return self
    
    def with_peak_reverse_torque_current(self, new_peak_reverse_torque_current: float) -> 'TorqueCurrentConfigs':
        """
        Modifies this configuration's peak_reverse_torque_current parameter and returns itself for
        method-chaining and easier to use config API.
    
        Minimum (reverse) output during torque current based control modes.
        
            - Minimum Value: -800
            - Maximum Value: 800
            - Default Value: -800
            - Units: A
    
        :param new_peak_reverse_torque_current: Parameter to modify
        :type new_peak_reverse_torque_current: float
        :returns: Itself
        :rtype: TorqueCurrentConfigs
        """
        self.peak_reverse_torque_current = new_peak_reverse_torque_current
        return self
    
    def with_torque_neutral_deadband(self, new_torque_neutral_deadband: float) -> 'TorqueCurrentConfigs':
        """
        Modifies this configuration's torque_neutral_deadband parameter and returns itself for
        method-chaining and easier to use config API.
    
        Configures the output deadband during torque current based control
        modes.
        
            - Minimum Value: 0
            - Maximum Value: 25
            - Default Value: 0.0
            - Units: A
    
        :param new_torque_neutral_deadband: Parameter to modify
        :type new_torque_neutral_deadband: float
        :returns: Itself
        :rtype: TorqueCurrentConfigs
        """
        self.torque_neutral_deadband = new_torque_neutral_deadband
        return self
    


    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: TorqueCurrent")
        ss.append("Name: \"PeakForwardTorqueCurrent\" Value: \"" + str(self.peak_forward_torque_current) + "A\"")
        ss.append("Name: \"PeakReverseTorqueCurrent\" Value: \"" + str(self.peak_reverse_torque_current) + "A\"")
        ss.append("Name: \"TorqueNeutralDeadband\" Value: \"" + str(self.torque_neutral_deadband) + "A\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_PEAK_FOR_TORQ_CURR.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.peak_forward_torque_current = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_PEAK_REV_TORQ_CURR.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.peak_reverse_torque_current = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_TORQUE_NEUTRAL_DB.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.torque_neutral_deadband = value.value
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_PEAK_FOR_TORQ_CURR.value, self.peak_forward_torque_current, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_PEAK_REV_TORQ_CURR.value, self.peak_reverse_torque_current, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_TORQUE_NEUTRAL_DB.value, self.torque_neutral_deadband, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)


class FeedbackConfigs:
    """
    Configs that affect the feedback of this motor controller.
    
    Includes feedback sensor source, any offsets for the feedback sensor,
    and various ratios to describe the relationship between the sensor and
    the mechanism for closed looping.
    """

    def __init__(self):
        self.feedback_rotor_offset: float = 0.0
        """
        This offset is applied to the absolute integrated rotor sensor.  This
        can be used to zero the rotor in applications that are within one
        rotor rotation.
        
            - Minimum Value: -1
            - Maximum Value: 1
            - Default Value: 0.0
            - Units: rotations
        """
        self.sensor_to_mechanism_ratio: float = 1.0
        """
        This is the ratio of sensor rotations to the mechanism's output.  This
        is equivalent to the mechanism's gear ratio if the sensor is located
        on the input of a gearbox.  If sensor is on the output of a gearbox,
        then this is typically set to 1.  Note if this is set to zero, device
        will reset back to one.
        
            - Minimum Value: -1000
            - Maximum Value: 1000
            - Default Value: 1.0
            - Units: scalar
        """
        self.rotor_to_sensor_ratio: float = 1.0
        """
        Talon FX is capable of fusing a remote CANcoder with its rotor sensor
        to produce a high-bandwidth sensor source.  This feature requires
        specifying the ratio between the remote sensor and the motor rotor. 
        Note if this is set to zero, device will reset back to one.
        
            - Minimum Value: -1000
            - Maximum Value: 1000
            - Default Value: 1.0
            - Units: scalar
        """
        self.feedback_sensor_source: FeedbackSensorSourceValue = FeedbackSensorSourceValue.ROTOR_SENSOR
        """
        Choose what sensor source is reported via API and used by closed-loop
        and limit features.  The default is RotorSensor, which uses the
        internal rotor sensor in the Talon FX.
        
        Choose RemoteCANcoder to use another CANcoder on the same CAN bus
        (this also requires setting FeedbackRemoteSensorID).  Talon FX will
        update its position and velocity whenever CANcoder publishes its
        information on CAN bus.
        
        Choose FusedCANcoder (requires Phoenix Pro) and Talon FX will fuse
        another CANcoder's information with the internal rotor, which provides
        the best possible position and velocity for accuracy and bandwidth
        (this also requires setting FeedbackRemoteSensorID).  FusedCANcoder
        was developed for applications such as swerve-azimuth.
        
        Choose SyncCANcoder (requires Phoenix Pro) and Talon FX will
        synchronize its internal rotor position against another CANcoder, then
        continue to use the rotor sensor for closed loop control (this also
        requires setting FeedbackRemoteSensorID).  The TalonFX will report if
        its internal position differs significantly from the reported CANcoder
        position.  SyncCANcoder was developed for mechanisms where there is a
        risk of the CANcoder failing in such a way that it reports a position
        that does not match the mechanism, such as the sensor mounting
        assembly breaking off.
        
        Choose RemotePigeon2_Yaw, RemotePigeon2_Pitch, and RemotePigeon2_Roll
        to use another Pigeon2 on the same CAN bus (this also requires setting
        FeedbackRemoteSensorID).  Talon FX will update its position to match
        the selected value whenever Pigeon2 publishes its information on CAN
        bus. Note that the Talon FX position will be in rotations and not
        degrees.
        
        Note: When the feedback source is changed to FusedCANcoder, the Talon
        FX needs a period of time to fuse before sensor-based (soft-limit,
        closed loop, etc.) features are used. This period of time is
        determined by the update frequency of the CANcoder's Position signal.
        
        """
        self.feedback_remote_sensor_id: int = 0
        """
        Device ID of which remote device to use.  This is not used if the
        Sensor Source is the internal rotor sensor.
        
            - Minimum Value: 0
            - Maximum Value: 62
            - Default Value: 0
            - Units: 
        """
    
    def with_feedback_rotor_offset(self, new_feedback_rotor_offset: float) -> 'FeedbackConfigs':
        """
        Modifies this configuration's feedback_rotor_offset parameter and returns itself for
        method-chaining and easier to use config API.
    
        This offset is applied to the absolute integrated rotor sensor.  This
        can be used to zero the rotor in applications that are within one
        rotor rotation.
        
            - Minimum Value: -1
            - Maximum Value: 1
            - Default Value: 0.0
            - Units: rotations
    
        :param new_feedback_rotor_offset: Parameter to modify
        :type new_feedback_rotor_offset: float
        :returns: Itself
        :rtype: FeedbackConfigs
        """
        self.feedback_rotor_offset = new_feedback_rotor_offset
        return self
    
    def with_sensor_to_mechanism_ratio(self, new_sensor_to_mechanism_ratio: float) -> 'FeedbackConfigs':
        """
        Modifies this configuration's sensor_to_mechanism_ratio parameter and returns itself for
        method-chaining and easier to use config API.
    
        This is the ratio of sensor rotations to the mechanism's output.  This
        is equivalent to the mechanism's gear ratio if the sensor is located
        on the input of a gearbox.  If sensor is on the output of a gearbox,
        then this is typically set to 1.  Note if this is set to zero, device
        will reset back to one.
        
            - Minimum Value: -1000
            - Maximum Value: 1000
            - Default Value: 1.0
            - Units: scalar
    
        :param new_sensor_to_mechanism_ratio: Parameter to modify
        :type new_sensor_to_mechanism_ratio: float
        :returns: Itself
        :rtype: FeedbackConfigs
        """
        self.sensor_to_mechanism_ratio = new_sensor_to_mechanism_ratio
        return self
    
    def with_rotor_to_sensor_ratio(self, new_rotor_to_sensor_ratio: float) -> 'FeedbackConfigs':
        """
        Modifies this configuration's rotor_to_sensor_ratio parameter and returns itself for
        method-chaining and easier to use config API.
    
        Talon FX is capable of fusing a remote CANcoder with its rotor sensor
        to produce a high-bandwidth sensor source.  This feature requires
        specifying the ratio between the remote sensor and the motor rotor. 
        Note if this is set to zero, device will reset back to one.
        
            - Minimum Value: -1000
            - Maximum Value: 1000
            - Default Value: 1.0
            - Units: scalar
    
        :param new_rotor_to_sensor_ratio: Parameter to modify
        :type new_rotor_to_sensor_ratio: float
        :returns: Itself
        :rtype: FeedbackConfigs
        """
        self.rotor_to_sensor_ratio = new_rotor_to_sensor_ratio
        return self
    
    def with_feedback_sensor_source(self, new_feedback_sensor_source: FeedbackSensorSourceValue) -> 'FeedbackConfigs':
        """
        Modifies this configuration's feedback_sensor_source parameter and returns itself for
        method-chaining and easier to use config API.
    
        Choose what sensor source is reported via API and used by closed-loop
        and limit features.  The default is RotorSensor, which uses the
        internal rotor sensor in the Talon FX.
        
        Choose RemoteCANcoder to use another CANcoder on the same CAN bus
        (this also requires setting FeedbackRemoteSensorID).  Talon FX will
        update its position and velocity whenever CANcoder publishes its
        information on CAN bus.
        
        Choose FusedCANcoder (requires Phoenix Pro) and Talon FX will fuse
        another CANcoder's information with the internal rotor, which provides
        the best possible position and velocity for accuracy and bandwidth
        (this also requires setting FeedbackRemoteSensorID).  FusedCANcoder
        was developed for applications such as swerve-azimuth.
        
        Choose SyncCANcoder (requires Phoenix Pro) and Talon FX will
        synchronize its internal rotor position against another CANcoder, then
        continue to use the rotor sensor for closed loop control (this also
        requires setting FeedbackRemoteSensorID).  The TalonFX will report if
        its internal position differs significantly from the reported CANcoder
        position.  SyncCANcoder was developed for mechanisms where there is a
        risk of the CANcoder failing in such a way that it reports a position
        that does not match the mechanism, such as the sensor mounting
        assembly breaking off.
        
        Choose RemotePigeon2_Yaw, RemotePigeon2_Pitch, and RemotePigeon2_Roll
        to use another Pigeon2 on the same CAN bus (this also requires setting
        FeedbackRemoteSensorID).  Talon FX will update its position to match
        the selected value whenever Pigeon2 publishes its information on CAN
        bus. Note that the Talon FX position will be in rotations and not
        degrees.
        
        Note: When the feedback source is changed to FusedCANcoder, the Talon
        FX needs a period of time to fuse before sensor-based (soft-limit,
        closed loop, etc.) features are used. This period of time is
        determined by the update frequency of the CANcoder's Position signal.
        
    
        :param new_feedback_sensor_source: Parameter to modify
        :type new_feedback_sensor_source: FeedbackSensorSourceValue
        :returns: Itself
        :rtype: FeedbackConfigs
        """
        self.feedback_sensor_source = new_feedback_sensor_source
        return self
    
    def with_feedback_remote_sensor_id(self, new_feedback_remote_sensor_id: int) -> 'FeedbackConfigs':
        """
        Modifies this configuration's feedback_remote_sensor_id parameter and returns itself for
        method-chaining and easier to use config API.
    
        Device ID of which remote device to use.  This is not used if the
        Sensor Source is the internal rotor sensor.
        
            - Minimum Value: 0
            - Maximum Value: 62
            - Default Value: 0
            - Units: 
    
        :param new_feedback_remote_sensor_id: Parameter to modify
        :type new_feedback_remote_sensor_id: int
        :returns: Itself
        :rtype: FeedbackConfigs
        """
        self.feedback_remote_sensor_id = new_feedback_remote_sensor_id
        return self
    

    
    
    
    
    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: Feedback")
        ss.append("Name: \"FeedbackRotorOffset\" Value: \"" + str(self.feedback_rotor_offset) + "rotations\"")
        ss.append("Name: \"SensorToMechanismRatio\" Value: \"" + str(self.sensor_to_mechanism_ratio) + "scalar\"")
        ss.append("Name: \"RotorToSensorRatio\" Value: \"" + str(self.rotor_to_sensor_ratio) + "scalar\"")
        ss.append("Name: \"FeedbackSensorSource\" Value: \"" + str(self.feedback_sensor_source) + "\"")
        ss.append("Name: \"FeedbackRemoteSensorID\" Value: \"" + str(self.feedback_remote_sensor_id) + "\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_FEEDBACK_ROTOR_OFFSET.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.feedback_rotor_offset = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_SENSOR_TO_MECHANISM_RATIO.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.sensor_to_mechanism_ratio = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_ROTOR_TO_SENSOR_RATIO.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.rotor_to_sensor_ratio = value.value
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.CONFIG_FEEDBACK_SENSOR_SOURCE.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.feedback_sensor_source = FeedbackSensorSourceValue(value.value)
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.CONFIG_FEEDBACK_REMOTE_SENSOR_ID.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.feedback_remote_sensor_id = value.value
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_FEEDBACK_ROTOR_OFFSET.value, self.feedback_rotor_offset, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_SENSOR_TO_MECHANISM_RATIO.value, self.sensor_to_mechanism_ratio, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_ROTOR_TO_SENSOR_RATIO.value, self.rotor_to_sensor_ratio, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.CONFIG_FEEDBACK_SENSOR_SOURCE.value, self.feedback_sensor_source.value, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.CONFIG_FEEDBACK_REMOTE_SENSOR_ID.value, self.feedback_remote_sensor_id, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)


class DifferentialSensorsConfigs:
    """
    Configs related to sensors used for differential control of a
    mechanism.
    
    Includes the differential sensor sources and IDs.
    """

    def __init__(self):
        self.differential_sensor_source: DifferentialSensorSourceValue = DifferentialSensorSourceValue.DISABLED
        """
        Choose what sensor source is used for differential control of a
        mechanism.  The default is Disabled.  All other options require
        setting the DifferentialTalonFXSensorID, as the average of this Talon
        FX's sensor and the remote TalonFX's sensor is used for the
        differential controller's primary targets.
        
        Choose RemoteTalonFX_Diff to use another TalonFX on the same CAN bus. 
        Talon FX will update its differential position and velocity whenever
        the remote TalonFX publishes its information on CAN bus.  The
        differential controller will use the difference between this TalonFX's
        sensor and the remote Talon FX's sensor for the differential component
        of the output.
        
        Choose RemotePigeon2_Yaw, RemotePigeon2_Pitch, and RemotePigeon2_Roll
        to use another Pigeon2 on the same CAN bus (this also requires setting
        DifferentialRemoteSensorID).  Talon FX will update its differential
        position to match the selected value whenever Pigeon2 publishes its
        information on CAN bus. Note that the Talon FX differential position
        will be in rotations and not degrees.
        
        Choose RemoteCANcoder to use another CANcoder on the same CAN bus
        (this also requires setting DifferentialRemoteSensorID).  Talon FX
        will update its differential position and velocity to match the
        CANcoder whenever CANcoder publishes its information on CAN bus.
        
        """
        self.differential_talon_fx_sensor_id: int = 0
        """
        Device ID of which remote Talon FX to use.  This is used when the
        Differential Sensor Source is not disabled.
        
            - Minimum Value: 0
            - Maximum Value: 62
            - Default Value: 0
            - Units: 
        """
        self.differential_remote_sensor_id: int = 0
        """
        Device ID of which remote sensor to use on the differential axis. 
        This is used when the Differential Sensor Source is not
        RemoteTalonFX_Diff.
        
            - Minimum Value: 0
            - Maximum Value: 62
            - Default Value: 0
            - Units: 
        """
    
    def with_differential_sensor_source(self, new_differential_sensor_source: DifferentialSensorSourceValue) -> 'DifferentialSensorsConfigs':
        """
        Modifies this configuration's differential_sensor_source parameter and returns itself for
        method-chaining and easier to use config API.
    
        Choose what sensor source is used for differential control of a
        mechanism.  The default is Disabled.  All other options require
        setting the DifferentialTalonFXSensorID, as the average of this Talon
        FX's sensor and the remote TalonFX's sensor is used for the
        differential controller's primary targets.
        
        Choose RemoteTalonFX_Diff to use another TalonFX on the same CAN bus. 
        Talon FX will update its differential position and velocity whenever
        the remote TalonFX publishes its information on CAN bus.  The
        differential controller will use the difference between this TalonFX's
        sensor and the remote Talon FX's sensor for the differential component
        of the output.
        
        Choose RemotePigeon2_Yaw, RemotePigeon2_Pitch, and RemotePigeon2_Roll
        to use another Pigeon2 on the same CAN bus (this also requires setting
        DifferentialRemoteSensorID).  Talon FX will update its differential
        position to match the selected value whenever Pigeon2 publishes its
        information on CAN bus. Note that the Talon FX differential position
        will be in rotations and not degrees.
        
        Choose RemoteCANcoder to use another CANcoder on the same CAN bus
        (this also requires setting DifferentialRemoteSensorID).  Talon FX
        will update its differential position and velocity to match the
        CANcoder whenever CANcoder publishes its information on CAN bus.
        
    
        :param new_differential_sensor_source: Parameter to modify
        :type new_differential_sensor_source: DifferentialSensorSourceValue
        :returns: Itself
        :rtype: DifferentialSensorsConfigs
        """
        self.differential_sensor_source = new_differential_sensor_source
        return self
    
    def with_differential_talon_fx_sensor_id(self, new_differential_talon_fx_sensor_id: int) -> 'DifferentialSensorsConfigs':
        """
        Modifies this configuration's differential_talon_fx_sensor_id parameter and returns itself for
        method-chaining and easier to use config API.
    
        Device ID of which remote Talon FX to use.  This is used when the
        Differential Sensor Source is not disabled.
        
            - Minimum Value: 0
            - Maximum Value: 62
            - Default Value: 0
            - Units: 
    
        :param new_differential_talon_fx_sensor_id: Parameter to modify
        :type new_differential_talon_fx_sensor_id: int
        :returns: Itself
        :rtype: DifferentialSensorsConfigs
        """
        self.differential_talon_fx_sensor_id = new_differential_talon_fx_sensor_id
        return self
    
    def with_differential_remote_sensor_id(self, new_differential_remote_sensor_id: int) -> 'DifferentialSensorsConfigs':
        """
        Modifies this configuration's differential_remote_sensor_id parameter and returns itself for
        method-chaining and easier to use config API.
    
        Device ID of which remote sensor to use on the differential axis. 
        This is used when the Differential Sensor Source is not
        RemoteTalonFX_Diff.
        
            - Minimum Value: 0
            - Maximum Value: 62
            - Default Value: 0
            - Units: 
    
        :param new_differential_remote_sensor_id: Parameter to modify
        :type new_differential_remote_sensor_id: int
        :returns: Itself
        :rtype: DifferentialSensorsConfigs
        """
        self.differential_remote_sensor_id = new_differential_remote_sensor_id
        return self
    


    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: DifferentialSensors")
        ss.append("Name: \"DifferentialSensorSource\" Value: \"" + str(self.differential_sensor_source) + "\"")
        ss.append("Name: \"DifferentialTalonFXSensorID\" Value: \"" + str(self.differential_talon_fx_sensor_id) + "\"")
        ss.append("Name: \"DifferentialRemoteSensorID\" Value: \"" + str(self.differential_remote_sensor_id) + "\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.CONFIG_DIFFERENTIAL_SENSOR_SOURCE.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.differential_sensor_source = DifferentialSensorSourceValue(value.value)
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.CONFIG_DIFFERENTIAL_TALON_FXSENSOR_ID.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.differential_talon_fx_sensor_id = value.value
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.CONFIG_DIFFERENTIAL_REMOTE_SENSOR_ID.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.differential_remote_sensor_id = value.value
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.CONFIG_DIFFERENTIAL_SENSOR_SOURCE.value, self.differential_sensor_source.value, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.CONFIG_DIFFERENTIAL_TALON_FXSENSOR_ID.value, self.differential_talon_fx_sensor_id, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.CONFIG_DIFFERENTIAL_REMOTE_SENSOR_ID.value, self.differential_remote_sensor_id, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)


class DifferentialConstantsConfigs:
    """
    Configs related to constants used for differential control of a
    mechanism.
    
    Includes the differential peak outputs.
    """

    def __init__(self):
        self.peak_differential_duty_cycle: float = 2
        """
        Maximum differential output during duty cycle based differential
        control modes.
        
            - Minimum Value: 0.0
            - Maximum Value: 2.0
            - Default Value: 2
            - Units: fractional
        """
        self.peak_differential_voltage: float = 32
        """
        Maximum differential output during voltage based differential control
        modes.
        
            - Minimum Value: 0.0
            - Maximum Value: 32
            - Default Value: 32
            - Units: V
        """
        self.peak_differential_torque_current: float = 1600
        """
        Maximum differential output during torque current based differential
        control modes.
        
            - Minimum Value: 0.0
            - Maximum Value: 1600
            - Default Value: 1600
            - Units: A
        """
    
    def with_peak_differential_duty_cycle(self, new_peak_differential_duty_cycle: float) -> 'DifferentialConstantsConfigs':
        """
        Modifies this configuration's peak_differential_duty_cycle parameter and returns itself for
        method-chaining and easier to use config API.
    
        Maximum differential output during duty cycle based differential
        control modes.
        
            - Minimum Value: 0.0
            - Maximum Value: 2.0
            - Default Value: 2
            - Units: fractional
    
        :param new_peak_differential_duty_cycle: Parameter to modify
        :type new_peak_differential_duty_cycle: float
        :returns: Itself
        :rtype: DifferentialConstantsConfigs
        """
        self.peak_differential_duty_cycle = new_peak_differential_duty_cycle
        return self
    
    def with_peak_differential_voltage(self, new_peak_differential_voltage: float) -> 'DifferentialConstantsConfigs':
        """
        Modifies this configuration's peak_differential_voltage parameter and returns itself for
        method-chaining and easier to use config API.
    
        Maximum differential output during voltage based differential control
        modes.
        
            - Minimum Value: 0.0
            - Maximum Value: 32
            - Default Value: 32
            - Units: V
    
        :param new_peak_differential_voltage: Parameter to modify
        :type new_peak_differential_voltage: float
        :returns: Itself
        :rtype: DifferentialConstantsConfigs
        """
        self.peak_differential_voltage = new_peak_differential_voltage
        return self
    
    def with_peak_differential_torque_current(self, new_peak_differential_torque_current: float) -> 'DifferentialConstantsConfigs':
        """
        Modifies this configuration's peak_differential_torque_current parameter and returns itself for
        method-chaining and easier to use config API.
    
        Maximum differential output during torque current based differential
        control modes.
        
            - Minimum Value: 0.0
            - Maximum Value: 1600
            - Default Value: 1600
            - Units: A
    
        :param new_peak_differential_torque_current: Parameter to modify
        :type new_peak_differential_torque_current: float
        :returns: Itself
        :rtype: DifferentialConstantsConfigs
        """
        self.peak_differential_torque_current = new_peak_differential_torque_current
        return self
    


    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: DifferentialConstants")
        ss.append("Name: \"PeakDifferentialDutyCycle\" Value: \"" + str(self.peak_differential_duty_cycle) + "fractional\"")
        ss.append("Name: \"PeakDifferentialVoltage\" Value: \"" + str(self.peak_differential_voltage) + "V\"")
        ss.append("Name: \"PeakDifferentialTorqueCurrent\" Value: \"" + str(self.peak_differential_torque_current) + "A\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_PEAK_DIFF_DC.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.peak_differential_duty_cycle = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_PEAK_DIFFV.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.peak_differential_voltage = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_PEAK_DIFF_TORQ_CURR.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.peak_differential_torque_current = value.value
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_PEAK_DIFF_DC.value, self.peak_differential_duty_cycle, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_PEAK_DIFFV.value, self.peak_differential_voltage, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_PEAK_DIFF_TORQ_CURR.value, self.peak_differential_torque_current, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)


class OpenLoopRampsConfigs:
    """
    Configs that affect the open-loop control of this motor controller.
    
    Open-loop ramp rates for the various control types.
    """

    def __init__(self):
        self.duty_cycle_open_loop_ramp_period: float = 0
        """
        If non-zero, this determines how much time to ramp from 0% output to
        100% during open-loop modes.
        
            - Minimum Value: 0
            - Maximum Value: 1
            - Default Value: 0
            - Units: sec
        """
        self.voltage_open_loop_ramp_period: float = 0
        """
        If non-zero, this determines how much time to ramp from 0V output to
        12V during open-loop modes.
        
            - Minimum Value: 0
            - Maximum Value: 1
            - Default Value: 0
            - Units: sec
        """
        self.torque_open_loop_ramp_period: float = 0
        """
        If non-zero, this determines how much time to ramp from 0A output to
        300A during open-loop modes.
        
            - Minimum Value: 0
            - Maximum Value: 10
            - Default Value: 0
            - Units: sec
        """
    
    def with_duty_cycle_open_loop_ramp_period(self, new_duty_cycle_open_loop_ramp_period: float) -> 'OpenLoopRampsConfigs':
        """
        Modifies this configuration's duty_cycle_open_loop_ramp_period parameter and returns itself for
        method-chaining and easier to use config API.
    
        If non-zero, this determines how much time to ramp from 0% output to
        100% during open-loop modes.
        
            - Minimum Value: 0
            - Maximum Value: 1
            - Default Value: 0
            - Units: sec
    
        :param new_duty_cycle_open_loop_ramp_period: Parameter to modify
        :type new_duty_cycle_open_loop_ramp_period: float
        :returns: Itself
        :rtype: OpenLoopRampsConfigs
        """
        self.duty_cycle_open_loop_ramp_period = new_duty_cycle_open_loop_ramp_period
        return self
    
    def with_voltage_open_loop_ramp_period(self, new_voltage_open_loop_ramp_period: float) -> 'OpenLoopRampsConfigs':
        """
        Modifies this configuration's voltage_open_loop_ramp_period parameter and returns itself for
        method-chaining and easier to use config API.
    
        If non-zero, this determines how much time to ramp from 0V output to
        12V during open-loop modes.
        
            - Minimum Value: 0
            - Maximum Value: 1
            - Default Value: 0
            - Units: sec
    
        :param new_voltage_open_loop_ramp_period: Parameter to modify
        :type new_voltage_open_loop_ramp_period: float
        :returns: Itself
        :rtype: OpenLoopRampsConfigs
        """
        self.voltage_open_loop_ramp_period = new_voltage_open_loop_ramp_period
        return self
    
    def with_torque_open_loop_ramp_period(self, new_torque_open_loop_ramp_period: float) -> 'OpenLoopRampsConfigs':
        """
        Modifies this configuration's torque_open_loop_ramp_period parameter and returns itself for
        method-chaining and easier to use config API.
    
        If non-zero, this determines how much time to ramp from 0A output to
        300A during open-loop modes.
        
            - Minimum Value: 0
            - Maximum Value: 10
            - Default Value: 0
            - Units: sec
    
        :param new_torque_open_loop_ramp_period: Parameter to modify
        :type new_torque_open_loop_ramp_period: float
        :returns: Itself
        :rtype: OpenLoopRampsConfigs
        """
        self.torque_open_loop_ramp_period = new_torque_open_loop_ramp_period
        return self
    


    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: OpenLoopRamps")
        ss.append("Name: \"DutyCycleOpenLoopRampPeriod\" Value: \"" + str(self.duty_cycle_open_loop_ramp_period) + "sec\"")
        ss.append("Name: \"VoltageOpenLoopRampPeriod\" Value: \"" + str(self.voltage_open_loop_ramp_period) + "sec\"")
        ss.append("Name: \"TorqueOpenLoopRampPeriod\" Value: \"" + str(self.torque_open_loop_ramp_period) + "sec\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_DUTY_CYCLE_OPEN_LOOP_RAMP_PERIOD.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.duty_cycle_open_loop_ramp_period = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_VOLTAGE_OPEN_LOOP_RAMP_PERIOD.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.voltage_open_loop_ramp_period = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_TORQUE_OPEN_LOOP_RAMP_PERIOD.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.torque_open_loop_ramp_period = value.value
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_DUTY_CYCLE_OPEN_LOOP_RAMP_PERIOD.value, self.duty_cycle_open_loop_ramp_period, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_VOLTAGE_OPEN_LOOP_RAMP_PERIOD.value, self.voltage_open_loop_ramp_period, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_TORQUE_OPEN_LOOP_RAMP_PERIOD.value, self.torque_open_loop_ramp_period, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)


class ClosedLoopRampsConfigs:
    """
    Configs that affect the closed-loop control of this motor controller.
    
    Closed-loop ramp rates for the various control types.
    """

    def __init__(self):
        self.duty_cycle_closed_loop_ramp_period: float = 0
        """
        If non-zero, this determines how much time to ramp from 0% output to
        100% during closed-loop modes.
        
            - Minimum Value: 0
            - Maximum Value: 1
            - Default Value: 0
            - Units: sec
        """
        self.voltage_closed_loop_ramp_period: float = 0
        """
        If non-zero, this determines how much time to ramp from 0V output to
        12V during closed-loop modes.
        
            - Minimum Value: 0
            - Maximum Value: 1
            - Default Value: 0
            - Units: sec
        """
        self.torque_closed_loop_ramp_period: float = 0
        """
        If non-zero, this determines how much time to ramp from 0A output to
        300A during closed-loop modes.
        
            - Minimum Value: 0
            - Maximum Value: 10
            - Default Value: 0
            - Units: sec
        """
    
    def with_duty_cycle_closed_loop_ramp_period(self, new_duty_cycle_closed_loop_ramp_period: float) -> 'ClosedLoopRampsConfigs':
        """
        Modifies this configuration's duty_cycle_closed_loop_ramp_period parameter and returns itself for
        method-chaining and easier to use config API.
    
        If non-zero, this determines how much time to ramp from 0% output to
        100% during closed-loop modes.
        
            - Minimum Value: 0
            - Maximum Value: 1
            - Default Value: 0
            - Units: sec
    
        :param new_duty_cycle_closed_loop_ramp_period: Parameter to modify
        :type new_duty_cycle_closed_loop_ramp_period: float
        :returns: Itself
        :rtype: ClosedLoopRampsConfigs
        """
        self.duty_cycle_closed_loop_ramp_period = new_duty_cycle_closed_loop_ramp_period
        return self
    
    def with_voltage_closed_loop_ramp_period(self, new_voltage_closed_loop_ramp_period: float) -> 'ClosedLoopRampsConfigs':
        """
        Modifies this configuration's voltage_closed_loop_ramp_period parameter and returns itself for
        method-chaining and easier to use config API.
    
        If non-zero, this determines how much time to ramp from 0V output to
        12V during closed-loop modes.
        
            - Minimum Value: 0
            - Maximum Value: 1
            - Default Value: 0
            - Units: sec
    
        :param new_voltage_closed_loop_ramp_period: Parameter to modify
        :type new_voltage_closed_loop_ramp_period: float
        :returns: Itself
        :rtype: ClosedLoopRampsConfigs
        """
        self.voltage_closed_loop_ramp_period = new_voltage_closed_loop_ramp_period
        return self
    
    def with_torque_closed_loop_ramp_period(self, new_torque_closed_loop_ramp_period: float) -> 'ClosedLoopRampsConfigs':
        """
        Modifies this configuration's torque_closed_loop_ramp_period parameter and returns itself for
        method-chaining and easier to use config API.
    
        If non-zero, this determines how much time to ramp from 0A output to
        300A during closed-loop modes.
        
            - Minimum Value: 0
            - Maximum Value: 10
            - Default Value: 0
            - Units: sec
    
        :param new_torque_closed_loop_ramp_period: Parameter to modify
        :type new_torque_closed_loop_ramp_period: float
        :returns: Itself
        :rtype: ClosedLoopRampsConfigs
        """
        self.torque_closed_loop_ramp_period = new_torque_closed_loop_ramp_period
        return self
    


    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: ClosedLoopRamps")
        ss.append("Name: \"DutyCycleClosedLoopRampPeriod\" Value: \"" + str(self.duty_cycle_closed_loop_ramp_period) + "sec\"")
        ss.append("Name: \"VoltageClosedLoopRampPeriod\" Value: \"" + str(self.voltage_closed_loop_ramp_period) + "sec\"")
        ss.append("Name: \"TorqueClosedLoopRampPeriod\" Value: \"" + str(self.torque_closed_loop_ramp_period) + "sec\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_DUTY_CYCLE_CLOSED_LOOP_RAMP_PERIOD.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.duty_cycle_closed_loop_ramp_period = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_VOLTAGE_CLOSED_LOOP_RAMP_PERIOD.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.voltage_closed_loop_ramp_period = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_TORQUE_CLOSED_LOOP_RAMP_PERIOD.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.torque_closed_loop_ramp_period = value.value
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_DUTY_CYCLE_CLOSED_LOOP_RAMP_PERIOD.value, self.duty_cycle_closed_loop_ramp_period, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_VOLTAGE_CLOSED_LOOP_RAMP_PERIOD.value, self.voltage_closed_loop_ramp_period, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_TORQUE_CLOSED_LOOP_RAMP_PERIOD.value, self.torque_closed_loop_ramp_period, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)


class HardwareLimitSwitchConfigs:
    """
    Configs that change how the motor controller behaves under different
    limit switch states.
    
    Includes configs such as enabling limit switches, configuring the
    remote sensor ID, the source, and the position to set on limit.
    """

    def __init__(self):
        self.forward_limit_type: ForwardLimitTypeValue = ForwardLimitTypeValue.NORMALLY_OPEN
        """
        Determines if the forward limit switch is normally-open (default) or
        normally-closed.
        
        """
        self.forward_limit_autoset_position_enable: bool = False
        """
        If enabled, the position is automatically set to a specific value,
        specified by ForwardLimitAutosetPositionValue, when the forward limit
        switch is asserted.
        
            - Default Value: False
        """
        self.forward_limit_autoset_position_value: float = 0
        """
        The value to automatically set the position to when the forward limit
        switch is asserted.  This has no effect if
        ForwardLimitAutosetPositionEnable is false.
        
            - Minimum Value: -3.4e+38
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: rotations
        """
        self.forward_limit_enable: bool = True
        """
        If enabled, motor output is set to neutral when the forward limit
        switch is asserted and positive output is requested.
        
            - Default Value: True
        """
        self.forward_limit_source: ForwardLimitSourceValue = ForwardLimitSourceValue.LIMIT_SWITCH_PIN
        """
        Determines where to poll the forward limit switch.  This defaults to
        the forward limit switch pin on the limit switch connector.
        
        Choose RemoteTalonFX to use the forward limit switch attached to
        another Talon FX on the same CAN bus (this also requires setting
        ForwardLimitRemoteSensorID).
        
        Choose RemoteCANifier to use the forward limit switch attached to
        another CANifier on the same CAN bus (this also requires setting
        ForwardLimitRemoteSensorID).
        
        Choose RemoteCANcoder to use another CANcoder on the same CAN bus
        (this also requires setting ForwardLimitRemoteSensorID).  The forward
        limit will assert when the CANcoder magnet strength changes from BAD
        (red) to ADEQUATE (orange) or GOOD (green).
        
        """
        self.forward_limit_remote_sensor_id: int = 0
        """
        Device ID of the remote device if using remote limit switch features
        for the forward limit switch.
        
            - Minimum Value: 0
            - Maximum Value: 62
            - Default Value: 0
            - Units: 
        """
        self.reverse_limit_type: ReverseLimitTypeValue = ReverseLimitTypeValue.NORMALLY_OPEN
        """
        Determines if the reverse limit switch is normally-open (default) or
        normally-closed.
        
        """
        self.reverse_limit_autoset_position_enable: bool = False
        """
        If enabled, the position is automatically set to a specific value,
        specified by ReverseLimitAutosetPositionValue, when the reverse limit
        switch is asserted.
        
            - Default Value: False
        """
        self.reverse_limit_autoset_position_value: float = 0
        """
        The value to automatically set the position to when the reverse limit
        switch is asserted.  This has no effect if
        ReverseLimitAutosetPositionEnable is false.
        
            - Minimum Value: -3.4e+38
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: rotations
        """
        self.reverse_limit_enable: bool = True
        """
        If enabled, motor output is set to neutral when reverse limit switch
        is asseted and negative output is requested.
        
            - Default Value: True
        """
        self.reverse_limit_source: ReverseLimitSourceValue = ReverseLimitSourceValue.LIMIT_SWITCH_PIN
        """
        Determines where to poll the reverse limit switch.  This defaults to
        the reverse limit switch pin on the limit switch connector.
        
        Choose RemoteTalonFX to use the reverse limit switch attached to
        another Talon FX on the same CAN bus (this also requires setting
        ReverseLimitRemoteSensorID).
        
        Choose RemoteCANifier to use the reverse limit switch attached to
        another CANifier on the same CAN bus (this also requires setting
        ReverseLimitRemoteSensorID).
        
        Choose RemoteCANcoder to use another CANcoder on the same CAN bus
        (this also requires setting ReverseLimitRemoteSensorID).  The reverse
        limit will assert when the CANcoder magnet strength changes from BAD
        (red) to ADEQUATE (orange) or GOOD (green).
        
        """
        self.reverse_limit_remote_sensor_id: int = 0
        """
        Device ID of the remote device if using remote limit switch features
        for the reverse limit switch.
        
            - Minimum Value: 0
            - Maximum Value: 62
            - Default Value: 0
            - Units: 
        """
    
    def with_forward_limit_type(self, new_forward_limit_type: ForwardLimitTypeValue) -> 'HardwareLimitSwitchConfigs':
        """
        Modifies this configuration's forward_limit_type parameter and returns itself for
        method-chaining and easier to use config API.
    
        Determines if the forward limit switch is normally-open (default) or
        normally-closed.
        
    
        :param new_forward_limit_type: Parameter to modify
        :type new_forward_limit_type: ForwardLimitTypeValue
        :returns: Itself
        :rtype: HardwareLimitSwitchConfigs
        """
        self.forward_limit_type = new_forward_limit_type
        return self
    
    def with_forward_limit_autoset_position_enable(self, new_forward_limit_autoset_position_enable: bool) -> 'HardwareLimitSwitchConfigs':
        """
        Modifies this configuration's forward_limit_autoset_position_enable parameter and returns itself for
        method-chaining and easier to use config API.
    
        If enabled, the position is automatically set to a specific value,
        specified by ForwardLimitAutosetPositionValue, when the forward limit
        switch is asserted.
        
            - Default Value: False
    
        :param new_forward_limit_autoset_position_enable: Parameter to modify
        :type new_forward_limit_autoset_position_enable: bool
        :returns: Itself
        :rtype: HardwareLimitSwitchConfigs
        """
        self.forward_limit_autoset_position_enable = new_forward_limit_autoset_position_enable
        return self
    
    def with_forward_limit_autoset_position_value(self, new_forward_limit_autoset_position_value: float) -> 'HardwareLimitSwitchConfigs':
        """
        Modifies this configuration's forward_limit_autoset_position_value parameter and returns itself for
        method-chaining and easier to use config API.
    
        The value to automatically set the position to when the forward limit
        switch is asserted.  This has no effect if
        ForwardLimitAutosetPositionEnable is false.
        
            - Minimum Value: -3.4e+38
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: rotations
    
        :param new_forward_limit_autoset_position_value: Parameter to modify
        :type new_forward_limit_autoset_position_value: float
        :returns: Itself
        :rtype: HardwareLimitSwitchConfigs
        """
        self.forward_limit_autoset_position_value = new_forward_limit_autoset_position_value
        return self
    
    def with_forward_limit_enable(self, new_forward_limit_enable: bool) -> 'HardwareLimitSwitchConfigs':
        """
        Modifies this configuration's forward_limit_enable parameter and returns itself for
        method-chaining and easier to use config API.
    
        If enabled, motor output is set to neutral when the forward limit
        switch is asserted and positive output is requested.
        
            - Default Value: True
    
        :param new_forward_limit_enable: Parameter to modify
        :type new_forward_limit_enable: bool
        :returns: Itself
        :rtype: HardwareLimitSwitchConfigs
        """
        self.forward_limit_enable = new_forward_limit_enable
        return self
    
    def with_forward_limit_source(self, new_forward_limit_source: ForwardLimitSourceValue) -> 'HardwareLimitSwitchConfigs':
        """
        Modifies this configuration's forward_limit_source parameter and returns itself for
        method-chaining and easier to use config API.
    
        Determines where to poll the forward limit switch.  This defaults to
        the forward limit switch pin on the limit switch connector.
        
        Choose RemoteTalonFX to use the forward limit switch attached to
        another Talon FX on the same CAN bus (this also requires setting
        ForwardLimitRemoteSensorID).
        
        Choose RemoteCANifier to use the forward limit switch attached to
        another CANifier on the same CAN bus (this also requires setting
        ForwardLimitRemoteSensorID).
        
        Choose RemoteCANcoder to use another CANcoder on the same CAN bus
        (this also requires setting ForwardLimitRemoteSensorID).  The forward
        limit will assert when the CANcoder magnet strength changes from BAD
        (red) to ADEQUATE (orange) or GOOD (green).
        
    
        :param new_forward_limit_source: Parameter to modify
        :type new_forward_limit_source: ForwardLimitSourceValue
        :returns: Itself
        :rtype: HardwareLimitSwitchConfigs
        """
        self.forward_limit_source = new_forward_limit_source
        return self
    
    def with_forward_limit_remote_sensor_id(self, new_forward_limit_remote_sensor_id: int) -> 'HardwareLimitSwitchConfigs':
        """
        Modifies this configuration's forward_limit_remote_sensor_id parameter and returns itself for
        method-chaining and easier to use config API.
    
        Device ID of the remote device if using remote limit switch features
        for the forward limit switch.
        
            - Minimum Value: 0
            - Maximum Value: 62
            - Default Value: 0
            - Units: 
    
        :param new_forward_limit_remote_sensor_id: Parameter to modify
        :type new_forward_limit_remote_sensor_id: int
        :returns: Itself
        :rtype: HardwareLimitSwitchConfigs
        """
        self.forward_limit_remote_sensor_id = new_forward_limit_remote_sensor_id
        return self
    
    def with_reverse_limit_type(self, new_reverse_limit_type: ReverseLimitTypeValue) -> 'HardwareLimitSwitchConfigs':
        """
        Modifies this configuration's reverse_limit_type parameter and returns itself for
        method-chaining and easier to use config API.
    
        Determines if the reverse limit switch is normally-open (default) or
        normally-closed.
        
    
        :param new_reverse_limit_type: Parameter to modify
        :type new_reverse_limit_type: ReverseLimitTypeValue
        :returns: Itself
        :rtype: HardwareLimitSwitchConfigs
        """
        self.reverse_limit_type = new_reverse_limit_type
        return self
    
    def with_reverse_limit_autoset_position_enable(self, new_reverse_limit_autoset_position_enable: bool) -> 'HardwareLimitSwitchConfigs':
        """
        Modifies this configuration's reverse_limit_autoset_position_enable parameter and returns itself for
        method-chaining and easier to use config API.
    
        If enabled, the position is automatically set to a specific value,
        specified by ReverseLimitAutosetPositionValue, when the reverse limit
        switch is asserted.
        
            - Default Value: False
    
        :param new_reverse_limit_autoset_position_enable: Parameter to modify
        :type new_reverse_limit_autoset_position_enable: bool
        :returns: Itself
        :rtype: HardwareLimitSwitchConfigs
        """
        self.reverse_limit_autoset_position_enable = new_reverse_limit_autoset_position_enable
        return self
    
    def with_reverse_limit_autoset_position_value(self, new_reverse_limit_autoset_position_value: float) -> 'HardwareLimitSwitchConfigs':
        """
        Modifies this configuration's reverse_limit_autoset_position_value parameter and returns itself for
        method-chaining and easier to use config API.
    
        The value to automatically set the position to when the reverse limit
        switch is asserted.  This has no effect if
        ReverseLimitAutosetPositionEnable is false.
        
            - Minimum Value: -3.4e+38
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: rotations
    
        :param new_reverse_limit_autoset_position_value: Parameter to modify
        :type new_reverse_limit_autoset_position_value: float
        :returns: Itself
        :rtype: HardwareLimitSwitchConfigs
        """
        self.reverse_limit_autoset_position_value = new_reverse_limit_autoset_position_value
        return self
    
    def with_reverse_limit_enable(self, new_reverse_limit_enable: bool) -> 'HardwareLimitSwitchConfigs':
        """
        Modifies this configuration's reverse_limit_enable parameter and returns itself for
        method-chaining and easier to use config API.
    
        If enabled, motor output is set to neutral when reverse limit switch
        is asseted and negative output is requested.
        
            - Default Value: True
    
        :param new_reverse_limit_enable: Parameter to modify
        :type new_reverse_limit_enable: bool
        :returns: Itself
        :rtype: HardwareLimitSwitchConfigs
        """
        self.reverse_limit_enable = new_reverse_limit_enable
        return self
    
    def with_reverse_limit_source(self, new_reverse_limit_source: ReverseLimitSourceValue) -> 'HardwareLimitSwitchConfigs':
        """
        Modifies this configuration's reverse_limit_source parameter and returns itself for
        method-chaining and easier to use config API.
    
        Determines where to poll the reverse limit switch.  This defaults to
        the reverse limit switch pin on the limit switch connector.
        
        Choose RemoteTalonFX to use the reverse limit switch attached to
        another Talon FX on the same CAN bus (this also requires setting
        ReverseLimitRemoteSensorID).
        
        Choose RemoteCANifier to use the reverse limit switch attached to
        another CANifier on the same CAN bus (this also requires setting
        ReverseLimitRemoteSensorID).
        
        Choose RemoteCANcoder to use another CANcoder on the same CAN bus
        (this also requires setting ReverseLimitRemoteSensorID).  The reverse
        limit will assert when the CANcoder magnet strength changes from BAD
        (red) to ADEQUATE (orange) or GOOD (green).
        
    
        :param new_reverse_limit_source: Parameter to modify
        :type new_reverse_limit_source: ReverseLimitSourceValue
        :returns: Itself
        :rtype: HardwareLimitSwitchConfigs
        """
        self.reverse_limit_source = new_reverse_limit_source
        return self
    
    def with_reverse_limit_remote_sensor_id(self, new_reverse_limit_remote_sensor_id: int) -> 'HardwareLimitSwitchConfigs':
        """
        Modifies this configuration's reverse_limit_remote_sensor_id parameter and returns itself for
        method-chaining and easier to use config API.
    
        Device ID of the remote device if using remote limit switch features
        for the reverse limit switch.
        
            - Minimum Value: 0
            - Maximum Value: 62
            - Default Value: 0
            - Units: 
    
        :param new_reverse_limit_remote_sensor_id: Parameter to modify
        :type new_reverse_limit_remote_sensor_id: int
        :returns: Itself
        :rtype: HardwareLimitSwitchConfigs
        """
        self.reverse_limit_remote_sensor_id = new_reverse_limit_remote_sensor_id
        return self
    

    
    
    
    
    
    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: HardwareLimitSwitch")
        ss.append("Name: \"ForwardLimitType\" Value: \"" + str(self.forward_limit_type) + "\"")
        ss.append("Name: \"ForwardLimitAutosetPositionEnable\" Value: \"" + str(self.forward_limit_autoset_position_enable) + "\"")
        ss.append("Name: \"ForwardLimitAutosetPositionValue\" Value: \"" + str(self.forward_limit_autoset_position_value) + "rotations\"")
        ss.append("Name: \"ForwardLimitEnable\" Value: \"" + str(self.forward_limit_enable) + "\"")
        ss.append("Name: \"ForwardLimitSource\" Value: \"" + str(self.forward_limit_source) + "\"")
        ss.append("Name: \"ForwardLimitRemoteSensorID\" Value: \"" + str(self.forward_limit_remote_sensor_id) + "\"")
        ss.append("Name: \"ReverseLimitType\" Value: \"" + str(self.reverse_limit_type) + "\"")
        ss.append("Name: \"ReverseLimitAutosetPositionEnable\" Value: \"" + str(self.reverse_limit_autoset_position_enable) + "\"")
        ss.append("Name: \"ReverseLimitAutosetPositionValue\" Value: \"" + str(self.reverse_limit_autoset_position_value) + "rotations\"")
        ss.append("Name: \"ReverseLimitEnable\" Value: \"" + str(self.reverse_limit_enable) + "\"")
        ss.append("Name: \"ReverseLimitSource\" Value: \"" + str(self.reverse_limit_source) + "\"")
        ss.append("Name: \"ReverseLimitRemoteSensorID\" Value: \"" + str(self.reverse_limit_remote_sensor_id) + "\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.CONFIG_FORWARD_LIMIT_TYPE.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.forward_limit_type = ForwardLimitTypeValue(value.value)
        value = ctypes.c_bool()
        Native.instance().c_ctre_phoenix6_deserialize_bool(SpnValue.CONFIG_FORWARD_LIMIT_AUTOSET_POS_ENABLE.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.forward_limit_autoset_position_enable = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_FORWARD_LIMIT_AUTOSET_POS_VALUE.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.forward_limit_autoset_position_value = value.value
        value = ctypes.c_bool()
        Native.instance().c_ctre_phoenix6_deserialize_bool(SpnValue.CONFIG_FORWARD_LIMIT_ENABLE.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.forward_limit_enable = value.value
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.CONFIG_FORWARD_LIMIT_SOURCE.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.forward_limit_source = ForwardLimitSourceValue(value.value)
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.CONFIG_FORWARD_LIMIT_REMOTE_SENSOR_ID.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.forward_limit_remote_sensor_id = value.value
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.CONFIG_REVERSE_LIMIT_TYPE.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.reverse_limit_type = ReverseLimitTypeValue(value.value)
        value = ctypes.c_bool()
        Native.instance().c_ctre_phoenix6_deserialize_bool(SpnValue.CONFIG_REVERSE_LIMIT_AUTOSET_POS_ENABLE.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.reverse_limit_autoset_position_enable = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_REVERSE_LIMIT_AUTOSET_POS_VALUE.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.reverse_limit_autoset_position_value = value.value
        value = ctypes.c_bool()
        Native.instance().c_ctre_phoenix6_deserialize_bool(SpnValue.CONFIG_REVERSE_LIMIT_ENABLE.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.reverse_limit_enable = value.value
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.CONFIG_REVERSE_LIMIT_SOURCE.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.reverse_limit_source = ReverseLimitSourceValue(value.value)
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.CONFIG_REVERSE_LIMIT_REMOTE_SENSOR_ID.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.reverse_limit_remote_sensor_id = value.value
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.CONFIG_FORWARD_LIMIT_TYPE.value, self.forward_limit_type.value, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_bool(SpnValue.CONFIG_FORWARD_LIMIT_AUTOSET_POS_ENABLE.value, self.forward_limit_autoset_position_enable, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_FORWARD_LIMIT_AUTOSET_POS_VALUE.value, self.forward_limit_autoset_position_value, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_bool(SpnValue.CONFIG_FORWARD_LIMIT_ENABLE.value, self.forward_limit_enable, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.CONFIG_FORWARD_LIMIT_SOURCE.value, self.forward_limit_source.value, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.CONFIG_FORWARD_LIMIT_REMOTE_SENSOR_ID.value, self.forward_limit_remote_sensor_id, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.CONFIG_REVERSE_LIMIT_TYPE.value, self.reverse_limit_type.value, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_bool(SpnValue.CONFIG_REVERSE_LIMIT_AUTOSET_POS_ENABLE.value, self.reverse_limit_autoset_position_enable, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_REVERSE_LIMIT_AUTOSET_POS_VALUE.value, self.reverse_limit_autoset_position_value, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_bool(SpnValue.CONFIG_REVERSE_LIMIT_ENABLE.value, self.reverse_limit_enable, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.CONFIG_REVERSE_LIMIT_SOURCE.value, self.reverse_limit_source.value, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.CONFIG_REVERSE_LIMIT_REMOTE_SENSOR_ID.value, self.reverse_limit_remote_sensor_id, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)


class AudioConfigs:
    """
    Configs that affect audible components of the device.
    
    Includes configuration for the beep on boot.
    """

    def __init__(self):
        self.beep_on_boot: bool = True
        """
        If true, the TalonFX will beep during boot-up.  This is useful for
        general debugging, and defaults to true.  If rotor is moving during
        boot-up, the beep will not occur regardless of this setting.
        
            - Default Value: True
        """
        self.beep_on_config: bool = True
        """
        If true, the TalonFX will beep during configuration API calls if
        device is disabled.  This is useful for general debugging, and
        defaults to true.  Note that if the rotor is moving, the beep will not
        occur regardless of this setting.
        
            - Default Value: True
        """
        self.allow_music_dur_disable: bool = False
        """
        If true, the TalonFX will allow Orchestra and MusicTone requests
        during disabled state.  This can be used to address corner cases when
        music features are needed when disabled.  This setting defaults to
        false.  Note that if the rotor is moving, music features are always
        disabled regardless of this setting.
        
            - Default Value: False
        """
    
    def with_beep_on_boot(self, new_beep_on_boot: bool) -> 'AudioConfigs':
        """
        Modifies this configuration's beep_on_boot parameter and returns itself for
        method-chaining and easier to use config API.
    
        If true, the TalonFX will beep during boot-up.  This is useful for
        general debugging, and defaults to true.  If rotor is moving during
        boot-up, the beep will not occur regardless of this setting.
        
            - Default Value: True
    
        :param new_beep_on_boot: Parameter to modify
        :type new_beep_on_boot: bool
        :returns: Itself
        :rtype: AudioConfigs
        """
        self.beep_on_boot = new_beep_on_boot
        return self
    
    def with_beep_on_config(self, new_beep_on_config: bool) -> 'AudioConfigs':
        """
        Modifies this configuration's beep_on_config parameter and returns itself for
        method-chaining and easier to use config API.
    
        If true, the TalonFX will beep during configuration API calls if
        device is disabled.  This is useful for general debugging, and
        defaults to true.  Note that if the rotor is moving, the beep will not
        occur regardless of this setting.
        
            - Default Value: True
    
        :param new_beep_on_config: Parameter to modify
        :type new_beep_on_config: bool
        :returns: Itself
        :rtype: AudioConfigs
        """
        self.beep_on_config = new_beep_on_config
        return self
    
    def with_allow_music_dur_disable(self, new_allow_music_dur_disable: bool) -> 'AudioConfigs':
        """
        Modifies this configuration's allow_music_dur_disable parameter and returns itself for
        method-chaining and easier to use config API.
    
        If true, the TalonFX will allow Orchestra and MusicTone requests
        during disabled state.  This can be used to address corner cases when
        music features are needed when disabled.  This setting defaults to
        false.  Note that if the rotor is moving, music features are always
        disabled regardless of this setting.
        
            - Default Value: False
    
        :param new_allow_music_dur_disable: Parameter to modify
        :type new_allow_music_dur_disable: bool
        :returns: Itself
        :rtype: AudioConfigs
        """
        self.allow_music_dur_disable = new_allow_music_dur_disable
        return self
    


    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: Audio")
        ss.append("Name: \"BeepOnBoot\" Value: \"" + str(self.beep_on_boot) + "\"")
        ss.append("Name: \"BeepOnConfig\" Value: \"" + str(self.beep_on_config) + "\"")
        ss.append("Name: \"AllowMusicDurDisable\" Value: \"" + str(self.allow_music_dur_disable) + "\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_bool()
        Native.instance().c_ctre_phoenix6_deserialize_bool(SpnValue.CONFIG_BEEP_ON_BOOT.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.beep_on_boot = value.value
        value = ctypes.c_bool()
        Native.instance().c_ctre_phoenix6_deserialize_bool(SpnValue.CONFIG_BEEP_ON_CONFIG.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.beep_on_config = value.value
        value = ctypes.c_bool()
        Native.instance().c_ctre_phoenix6_deserialize_bool(SpnValue.CONFIG_ALLOW_MUSIC_DUR_DISABLE.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.allow_music_dur_disable = value.value
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_bool(SpnValue.CONFIG_BEEP_ON_BOOT.value, self.beep_on_boot, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_bool(SpnValue.CONFIG_BEEP_ON_CONFIG.value, self.beep_on_config, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_bool(SpnValue.CONFIG_ALLOW_MUSIC_DUR_DISABLE.value, self.allow_music_dur_disable, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)


class SoftwareLimitSwitchConfigs:
    """
    Configs that affect how software-limit switches behave.
    
    Includes enabling software-limit switches and the threshold at which
    they are tripped.
    """

    def __init__(self):
        self.forward_soft_limit_enable: bool = False
        """
        If enabled, the motor output is set to neutral if position exceeds
        ForwardSoftLimitThreshold and forward output is requested.
        
            - Default Value: False
        """
        self.reverse_soft_limit_enable: bool = False
        """
        If enabled, the motor output is set to neutral if position exceeds
        ReverseSoftLimitThreshold and reverse output is requested.
        
            - Default Value: False
        """
        self.forward_soft_limit_threshold: float = 0
        """
        Position threshold for forward soft limit features.
        ForwardSoftLimitEnable must be enabled for this to take effect.
        
            - Minimum Value: -3.4e+38
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: rotations
        """
        self.reverse_soft_limit_threshold: float = 0
        """
        Position threshold for reverse soft limit features.
        ReverseSoftLimitEnable must be enabled for this to take effect.
        
            - Minimum Value: -3.4e+38
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: rotations
        """
    
    def with_forward_soft_limit_enable(self, new_forward_soft_limit_enable: bool) -> 'SoftwareLimitSwitchConfigs':
        """
        Modifies this configuration's forward_soft_limit_enable parameter and returns itself for
        method-chaining and easier to use config API.
    
        If enabled, the motor output is set to neutral if position exceeds
        ForwardSoftLimitThreshold and forward output is requested.
        
            - Default Value: False
    
        :param new_forward_soft_limit_enable: Parameter to modify
        :type new_forward_soft_limit_enable: bool
        :returns: Itself
        :rtype: SoftwareLimitSwitchConfigs
        """
        self.forward_soft_limit_enable = new_forward_soft_limit_enable
        return self
    
    def with_reverse_soft_limit_enable(self, new_reverse_soft_limit_enable: bool) -> 'SoftwareLimitSwitchConfigs':
        """
        Modifies this configuration's reverse_soft_limit_enable parameter and returns itself for
        method-chaining and easier to use config API.
    
        If enabled, the motor output is set to neutral if position exceeds
        ReverseSoftLimitThreshold and reverse output is requested.
        
            - Default Value: False
    
        :param new_reverse_soft_limit_enable: Parameter to modify
        :type new_reverse_soft_limit_enable: bool
        :returns: Itself
        :rtype: SoftwareLimitSwitchConfigs
        """
        self.reverse_soft_limit_enable = new_reverse_soft_limit_enable
        return self
    
    def with_forward_soft_limit_threshold(self, new_forward_soft_limit_threshold: float) -> 'SoftwareLimitSwitchConfigs':
        """
        Modifies this configuration's forward_soft_limit_threshold parameter and returns itself for
        method-chaining and easier to use config API.
    
        Position threshold for forward soft limit features.
        ForwardSoftLimitEnable must be enabled for this to take effect.
        
            - Minimum Value: -3.4e+38
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: rotations
    
        :param new_forward_soft_limit_threshold: Parameter to modify
        :type new_forward_soft_limit_threshold: float
        :returns: Itself
        :rtype: SoftwareLimitSwitchConfigs
        """
        self.forward_soft_limit_threshold = new_forward_soft_limit_threshold
        return self
    
    def with_reverse_soft_limit_threshold(self, new_reverse_soft_limit_threshold: float) -> 'SoftwareLimitSwitchConfigs':
        """
        Modifies this configuration's reverse_soft_limit_threshold parameter and returns itself for
        method-chaining and easier to use config API.
    
        Position threshold for reverse soft limit features.
        ReverseSoftLimitEnable must be enabled for this to take effect.
        
            - Minimum Value: -3.4e+38
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: rotations
    
        :param new_reverse_soft_limit_threshold: Parameter to modify
        :type new_reverse_soft_limit_threshold: float
        :returns: Itself
        :rtype: SoftwareLimitSwitchConfigs
        """
        self.reverse_soft_limit_threshold = new_reverse_soft_limit_threshold
        return self
    


    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: SoftwareLimitSwitch")
        ss.append("Name: \"ForwardSoftLimitEnable\" Value: \"" + str(self.forward_soft_limit_enable) + "\"")
        ss.append("Name: \"ReverseSoftLimitEnable\" Value: \"" + str(self.reverse_soft_limit_enable) + "\"")
        ss.append("Name: \"ForwardSoftLimitThreshold\" Value: \"" + str(self.forward_soft_limit_threshold) + "rotations\"")
        ss.append("Name: \"ReverseSoftLimitThreshold\" Value: \"" + str(self.reverse_soft_limit_threshold) + "rotations\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_bool()
        Native.instance().c_ctre_phoenix6_deserialize_bool(SpnValue.CONFIG_FORWARD_SOFT_LIMIT_ENABLE.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.forward_soft_limit_enable = value.value
        value = ctypes.c_bool()
        Native.instance().c_ctre_phoenix6_deserialize_bool(SpnValue.CONFIG_REVERSE_SOFT_LIMIT_ENABLE.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.reverse_soft_limit_enable = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_FORWARD_SOFT_LIMIT_THRESHOLD.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.forward_soft_limit_threshold = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_REVERSE_SOFT_LIMIT_THRESHOLD.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.reverse_soft_limit_threshold = value.value
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_bool(SpnValue.CONFIG_FORWARD_SOFT_LIMIT_ENABLE.value, self.forward_soft_limit_enable, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_bool(SpnValue.CONFIG_REVERSE_SOFT_LIMIT_ENABLE.value, self.reverse_soft_limit_enable, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_FORWARD_SOFT_LIMIT_THRESHOLD.value, self.forward_soft_limit_threshold, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_REVERSE_SOFT_LIMIT_THRESHOLD.value, self.reverse_soft_limit_threshold, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)


class MotionMagicConfigs:
    """
    Configs for Motion Magic®.
    
    Includes Velocity, Acceleration, Jerk, and Expo parameters.
    """

    def __init__(self):
        self.motion_magic_cruise_velocity: float = 0
        """
        This is the maximum velocity Motion Magic® based control modes are
        allowed to use.  Motion Magic® Velocity control modes do not use this
        config.  When using Motion Magic® Expo control modes, setting this to
        0 will allow the profile to run to the max possible velocity based on
        Expo_kV.
        
            - Minimum Value: 0
            - Maximum Value: 9999
            - Default Value: 0
            - Units: rps
        """
        self.motion_magic_acceleration: float = 0
        """
        This is the target acceleration Motion Magic® based control modes are
        allowed to use.  Motion Magic® Expo control modes do not use this
        config.
        
            - Minimum Value: 0
            - Maximum Value: 9999
            - Default Value: 0
            - Units: rot per sec²
        """
        self.motion_magic_jerk: float = 0
        """
        This is the target jerk (acceleration derivative) Motion Magic® based
        control modes are allowed to use.  Motion Magic® Expo control modes do
        not use this config.  This allows Motion Magic® support of S-Curves. 
        If this is set to zero, then Motion Magic® will not apply a Jerk
        limit.
        
            - Minimum Value: 0
            - Maximum Value: 9999
            - Default Value: 0
            - Units: rot per sec³
        """
        self.motion_magic_expo_k_v: float = 0
        """
        This is the target kV used only by Motion Magic® Expo control modes,
        in units of V/rps. This represents the amount of voltage necessary to
        hold a velocity. In terms of the Motion Magic® Expo profile, a higher
        kV results in a slower maximum velocity. A kV of 0 will be promoted to
        a reasonable default of 0.12.
        
            - Minimum Value: 0.001
            - Maximum Value: 100
            - Default Value: 0
            - Units: V/rps
        """
        self.motion_magic_expo_k_a: float = 0
        """
        This is the target kA used only by Motion Magic® Expo control modes,
        in units of V/rps². This represents the amount of voltage necessary to
        achieve an acceleration. In terms of the Motion Magic® Expo profile, a
        higher kA results in a slower acceleration. A kA of 0 will be promoted
        to a reasonable default of 0.1.
        
            - Minimum Value: 1e-05
            - Maximum Value: 100
            - Default Value: 0
            - Units: V/rps²
        """
    
    def with_motion_magic_cruise_velocity(self, new_motion_magic_cruise_velocity: float) -> 'MotionMagicConfigs':
        """
        Modifies this configuration's motion_magic_cruise_velocity parameter and returns itself for
        method-chaining and easier to use config API.
    
        This is the maximum velocity Motion Magic® based control modes are
        allowed to use.  Motion Magic® Velocity control modes do not use this
        config.  When using Motion Magic® Expo control modes, setting this to
        0 will allow the profile to run to the max possible velocity based on
        Expo_kV.
        
            - Minimum Value: 0
            - Maximum Value: 9999
            - Default Value: 0
            - Units: rps
    
        :param new_motion_magic_cruise_velocity: Parameter to modify
        :type new_motion_magic_cruise_velocity: float
        :returns: Itself
        :rtype: MotionMagicConfigs
        """
        self.motion_magic_cruise_velocity = new_motion_magic_cruise_velocity
        return self
    
    def with_motion_magic_acceleration(self, new_motion_magic_acceleration: float) -> 'MotionMagicConfigs':
        """
        Modifies this configuration's motion_magic_acceleration parameter and returns itself for
        method-chaining and easier to use config API.
    
        This is the target acceleration Motion Magic® based control modes are
        allowed to use.  Motion Magic® Expo control modes do not use this
        config.
        
            - Minimum Value: 0
            - Maximum Value: 9999
            - Default Value: 0
            - Units: rot per sec²
    
        :param new_motion_magic_acceleration: Parameter to modify
        :type new_motion_magic_acceleration: float
        :returns: Itself
        :rtype: MotionMagicConfigs
        """
        self.motion_magic_acceleration = new_motion_magic_acceleration
        return self
    
    def with_motion_magic_jerk(self, new_motion_magic_jerk: float) -> 'MotionMagicConfigs':
        """
        Modifies this configuration's motion_magic_jerk parameter and returns itself for
        method-chaining and easier to use config API.
    
        This is the target jerk (acceleration derivative) Motion Magic® based
        control modes are allowed to use.  Motion Magic® Expo control modes do
        not use this config.  This allows Motion Magic® support of S-Curves. 
        If this is set to zero, then Motion Magic® will not apply a Jerk
        limit.
        
            - Minimum Value: 0
            - Maximum Value: 9999
            - Default Value: 0
            - Units: rot per sec³
    
        :param new_motion_magic_jerk: Parameter to modify
        :type new_motion_magic_jerk: float
        :returns: Itself
        :rtype: MotionMagicConfigs
        """
        self.motion_magic_jerk = new_motion_magic_jerk
        return self
    
    def with_motion_magic_expo_k_v(self, new_motion_magic_expo_k_v: float) -> 'MotionMagicConfigs':
        """
        Modifies this configuration's motion_magic_expo_k_v parameter and returns itself for
        method-chaining and easier to use config API.
    
        This is the target kV used only by Motion Magic® Expo control modes,
        in units of V/rps. This represents the amount of voltage necessary to
        hold a velocity. In terms of the Motion Magic® Expo profile, a higher
        kV results in a slower maximum velocity. A kV of 0 will be promoted to
        a reasonable default of 0.12.
        
            - Minimum Value: 0.001
            - Maximum Value: 100
            - Default Value: 0
            - Units: V/rps
    
        :param new_motion_magic_expo_k_v: Parameter to modify
        :type new_motion_magic_expo_k_v: float
        :returns: Itself
        :rtype: MotionMagicConfigs
        """
        self.motion_magic_expo_k_v = new_motion_magic_expo_k_v
        return self
    
    def with_motion_magic_expo_k_a(self, new_motion_magic_expo_k_a: float) -> 'MotionMagicConfigs':
        """
        Modifies this configuration's motion_magic_expo_k_a parameter and returns itself for
        method-chaining and easier to use config API.
    
        This is the target kA used only by Motion Magic® Expo control modes,
        in units of V/rps². This represents the amount of voltage necessary to
        achieve an acceleration. In terms of the Motion Magic® Expo profile, a
        higher kA results in a slower acceleration. A kA of 0 will be promoted
        to a reasonable default of 0.1.
        
            - Minimum Value: 1e-05
            - Maximum Value: 100
            - Default Value: 0
            - Units: V/rps²
    
        :param new_motion_magic_expo_k_a: Parameter to modify
        :type new_motion_magic_expo_k_a: float
        :returns: Itself
        :rtype: MotionMagicConfigs
        """
        self.motion_magic_expo_k_a = new_motion_magic_expo_k_a
        return self
    


    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: MotionMagic")
        ss.append("Name: \"MotionMagicCruiseVelocity\" Value: \"" + str(self.motion_magic_cruise_velocity) + "rps\"")
        ss.append("Name: \"MotionMagicAcceleration\" Value: \"" + str(self.motion_magic_acceleration) + "rot per sec²\"")
        ss.append("Name: \"MotionMagicJerk\" Value: \"" + str(self.motion_magic_jerk) + "rot per sec³\"")
        ss.append("Name: \"MotionMagicExpo_kV\" Value: \"" + str(self.motion_magic_expo_k_v) + "V/rps\"")
        ss.append("Name: \"MotionMagicExpo_kA\" Value: \"" + str(self.motion_magic_expo_k_a) + "V/rps²\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_MOTION_MAGIC_CRUISE_VELOCITY.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.motion_magic_cruise_velocity = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_MOTION_MAGIC_ACCELERATION.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.motion_magic_acceleration = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_MOTION_MAGIC_JERK.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.motion_magic_jerk = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_MOTION_MAGIC_EXPO_KV.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.motion_magic_expo_k_v = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.CONFIG_MOTION_MAGIC_EXPO_KA.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.motion_magic_expo_k_a = value.value
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_MOTION_MAGIC_CRUISE_VELOCITY.value, self.motion_magic_cruise_velocity, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_MOTION_MAGIC_ACCELERATION.value, self.motion_magic_acceleration, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_MOTION_MAGIC_JERK.value, self.motion_magic_jerk, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_MOTION_MAGIC_EXPO_KV.value, self.motion_magic_expo_k_v, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CONFIG_MOTION_MAGIC_EXPO_KA.value, self.motion_magic_expo_k_a, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)


class CustomParamsConfigs:
    """
    Custom Params.
    
    Custom paramaters that have no real impact on controller.
    """

    def __init__(self):
        self.custom_param0: int = 0
        """
        Custom parameter 0.  This is provided to allow end-applications to
        store persistent information in the device.
        
            - Minimum Value: -32768
            - Maximum Value: 32767
            - Default Value: 0
            - Units: 
        """
        self.custom_param1: int = 0
        """
        Custom parameter 1.  This is provided to allow end-applications to
        store persistent information in the device.
        
            - Minimum Value: -32768
            - Maximum Value: 32767
            - Default Value: 0
            - Units: 
        """
    
    def with_custom_param0(self, new_custom_param0: int) -> 'CustomParamsConfigs':
        """
        Modifies this configuration's custom_param0 parameter and returns itself for
        method-chaining and easier to use config API.
    
        Custom parameter 0.  This is provided to allow end-applications to
        store persistent information in the device.
        
            - Minimum Value: -32768
            - Maximum Value: 32767
            - Default Value: 0
            - Units: 
    
        :param new_custom_param0: Parameter to modify
        :type new_custom_param0: int
        :returns: Itself
        :rtype: CustomParamsConfigs
        """
        self.custom_param0 = new_custom_param0
        return self
    
    def with_custom_param1(self, new_custom_param1: int) -> 'CustomParamsConfigs':
        """
        Modifies this configuration's custom_param1 parameter and returns itself for
        method-chaining and easier to use config API.
    
        Custom parameter 1.  This is provided to allow end-applications to
        store persistent information in the device.
        
            - Minimum Value: -32768
            - Maximum Value: 32767
            - Default Value: 0
            - Units: 
    
        :param new_custom_param1: Parameter to modify
        :type new_custom_param1: int
        :returns: Itself
        :rtype: CustomParamsConfigs
        """
        self.custom_param1 = new_custom_param1
        return self
    


    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: CustomParams")
        ss.append("Name: \"CustomParam0\" Value: \"" + str(self.custom_param0) + "\"")
        ss.append("Name: \"CustomParam1\" Value: \"" + str(self.custom_param1) + "\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.CUSTOM_PARAM0.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.custom_param0 = value.value
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.CUSTOM_PARAM1.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.custom_param1 = value.value
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.CUSTOM_PARAM0.value, self.custom_param0, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.CUSTOM_PARAM1.value, self.custom_param1, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)


class ClosedLoopGeneralConfigs:
    """
    Configs that affect general behavior during closed-looping.
    
    Includes Continuous Wrap features.
    """

    def __init__(self):
        self.continuous_wrap: bool = False
        """
        Wrap position error within [-0.5,+0.5) mechanism rotations.  Typically
        used for continuous position closed-loops like swerve azimuth.
        
        This uses the mechanism rotation value. If there is a gear ratio
        between the sensor and the mechanism, make sure to apply a
        SensorToMechanismRatio so the closed loop operates on the full
        rotation.
        
            - Default Value: False
        """



    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: ClosedLoopGeneral")
        ss.append("Name: \"ContinuousWrap\" Value: \"" + str(self.continuous_wrap) + "\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_bool()
        Native.instance().c_ctre_phoenix6_deserialize_bool(SpnValue.CONFIG_CONTINUOUS_WRAP.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.continuous_wrap = value.value
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_bool(SpnValue.CONFIG_CONTINUOUS_WRAP.value, self.continuous_wrap, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)


class Slot0Configs:
    """
    Gains for the specified slot.
    
    If this slot is selected, these gains are used in closed loop control
    requests.
    """

    def __init__(self):
        self.k_p: float = 0
        """
        Proportional Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by error in the input, the units should be defined
        as units of output per unit of input error. For example, when
        controlling velocity using a duty cycle closed loop, the units for the
        proportional gain will be duty cycle per rps of error, or 1/rps.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
        """
        self.k_i: float = 0
        """
        Integral Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by error in the input integrated over time (in
        units of seconds), the units should be defined as units of output per
        unit of integrated input error. For example, when controlling velocity
        using a duty cycle closed loop, integrating velocity over time results
        in rps * s = rotations. Therefore, the units for the integral gain
        will be duty cycle per rotation of accumulated error, or 1/rot.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
        """
        self.k_d: float = 0
        """
        Derivative Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the derivative of error in the input with
        respect to time (in units of seconds), the units should be defined as
        units of output per unit of the differentiated input error. For
        example, when controlling velocity using a duty cycle closed loop, the
        derivative of velocity with respect to time is rps/s, which is
        acceleration. Therefore, the units for the derivative gain will be
        duty cycle per unit of acceleration error, or 1/(rps/s).
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
        """
        self.k_s: float = 0
        """
        Static Feedforward Gain
        
        This is added to the closed loop output. The unit for this constant is
        dependent on the control mode, typically fractional duty cycle,
        voltage, or torque current.
        
        The sign is typically determined by reference velocity when using
        position, velocity, and Motion Magic® closed loop modes. However, when
        using position closed loop with zero velocity reference (no motion
        profiling), the application can instead use the position closed loop
        error by setting the Static Feedforward Sign configuration parameter. 
        When doing so, we recommend the minimal amount of kS, otherwise the
        motor output may dither when closed loop error is near zero.
        
            - Minimum Value: -512
            - Maximum Value: 511
            - Default Value: 0
            - Units: 
        """
        self.k_v: float = 0
        """
        Velocity Feedforward Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the requested velocity, the units should be
        defined as units of output per unit of requested input velocity. For
        example, when controlling velocity using a duty cycle closed loop, the
        units for the velocity feedfoward gain will be duty cycle per
        requested rps, or 1/rps.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
        """
        self.k_a: float = 0
        """
        Acceleration Feedforward Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the requested acceleration, the units should be
        defined as units of output per unit of requested input acceleration.
        For example, when controlling velocity using a duty cycle closed loop,
        the units for the acceleration feedfoward gain will be duty cycle per
        requested rps/s, or 1/(rps/s).
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
        """
        self.k_g: float = 0
        """
        Gravity Feedforward/Feedback Gain
        
        This is added to the closed loop output. The sign is determined by
        GravityType. The unit for this constant is dependent on the control
        mode, typically fractional duty cycle, voltage, or torque current.
        
            - Minimum Value: -512
            - Maximum Value: 511
            - Default Value: 0
            - Units: 
        """
        self.gravity_type: GravityTypeValue = GravityTypeValue.ELEVATOR_STATIC
        """
        Gravity Feedforward/Feedback Type
        
        This determines the type of the gravity feedforward/feedback.
        
        Choose Elevator_Static for systems where the gravity feedforward is
        constant, such as an elevator. The gravity feedforward output will
        always have the same sign.
        
        Choose Arm_Cosine for systems where the gravity feedback is dependent
        on the angular position of the mechanism, such as an arm. The gravity
        feedback output will vary depending on the mechanism angular position.
        Note that the sensor offset and ratios must be configured so that the
        sensor reports a position of 0 when the mechanism is horizonal
        (parallel to the ground), and the reported sensor position is 1:1 with
        the mechanism.
        
        """
        self.static_feedforward_sign: StaticFeedforwardSignValue = StaticFeedforwardSignValue.USE_VELOCITY_SIGN
        """
        Static Feedforward Sign during position closed loop
        
        This determines the sign of the applied kS during position closed-loop
        modes. The default behavior uses the velocity reference sign. This
        works well with velocity closed loop, Motion Magic® controls, and
        position closed loop when velocity reference is specified (motion
        profiling).
        
        However, when using position closed loop with zero velocity reference
        (no motion profiling), the application may want to apply static
        feedforward based on the closed loop error sign instead. When doing
        so, we recommend the minimal amount of kS, otherwise the motor output
        may dither when closed loop error is near zero.
        
        """
    
    def with_k_p(self, new_k_p: float) -> 'Slot0Configs':
        """
        Modifies this configuration's k_p parameter and returns itself for
        method-chaining and easier to use config API.
    
        Proportional Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by error in the input, the units should be defined
        as units of output per unit of input error. For example, when
        controlling velocity using a duty cycle closed loop, the units for the
        proportional gain will be duty cycle per rps of error, or 1/rps.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
    
        :param new_k_p: Parameter to modify
        :type new_k_p: float
        :returns: Itself
        :rtype: Slot0Configs
        """
        self.k_p = new_k_p
        return self
    
    def with_k_i(self, new_k_i: float) -> 'Slot0Configs':
        """
        Modifies this configuration's k_i parameter and returns itself for
        method-chaining and easier to use config API.
    
        Integral Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by error in the input integrated over time (in
        units of seconds), the units should be defined as units of output per
        unit of integrated input error. For example, when controlling velocity
        using a duty cycle closed loop, integrating velocity over time results
        in rps * s = rotations. Therefore, the units for the integral gain
        will be duty cycle per rotation of accumulated error, or 1/rot.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
    
        :param new_k_i: Parameter to modify
        :type new_k_i: float
        :returns: Itself
        :rtype: Slot0Configs
        """
        self.k_i = new_k_i
        return self
    
    def with_k_d(self, new_k_d: float) -> 'Slot0Configs':
        """
        Modifies this configuration's k_d parameter and returns itself for
        method-chaining and easier to use config API.
    
        Derivative Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the derivative of error in the input with
        respect to time (in units of seconds), the units should be defined as
        units of output per unit of the differentiated input error. For
        example, when controlling velocity using a duty cycle closed loop, the
        derivative of velocity with respect to time is rps/s, which is
        acceleration. Therefore, the units for the derivative gain will be
        duty cycle per unit of acceleration error, or 1/(rps/s).
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
    
        :param new_k_d: Parameter to modify
        :type new_k_d: float
        :returns: Itself
        :rtype: Slot0Configs
        """
        self.k_d = new_k_d
        return self
    
    def with_k_s(self, new_k_s: float) -> 'Slot0Configs':
        """
        Modifies this configuration's k_s parameter and returns itself for
        method-chaining and easier to use config API.
    
        Static Feedforward Gain
        
        This is added to the closed loop output. The unit for this constant is
        dependent on the control mode, typically fractional duty cycle,
        voltage, or torque current.
        
        The sign is typically determined by reference velocity when using
        position, velocity, and Motion Magic® closed loop modes. However, when
        using position closed loop with zero velocity reference (no motion
        profiling), the application can instead use the position closed loop
        error by setting the Static Feedforward Sign configuration parameter. 
        When doing so, we recommend the minimal amount of kS, otherwise the
        motor output may dither when closed loop error is near zero.
        
            - Minimum Value: -512
            - Maximum Value: 511
            - Default Value: 0
            - Units: 
    
        :param new_k_s: Parameter to modify
        :type new_k_s: float
        :returns: Itself
        :rtype: Slot0Configs
        """
        self.k_s = new_k_s
        return self
    
    def with_k_v(self, new_k_v: float) -> 'Slot0Configs':
        """
        Modifies this configuration's k_v parameter and returns itself for
        method-chaining and easier to use config API.
    
        Velocity Feedforward Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the requested velocity, the units should be
        defined as units of output per unit of requested input velocity. For
        example, when controlling velocity using a duty cycle closed loop, the
        units for the velocity feedfoward gain will be duty cycle per
        requested rps, or 1/rps.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
    
        :param new_k_v: Parameter to modify
        :type new_k_v: float
        :returns: Itself
        :rtype: Slot0Configs
        """
        self.k_v = new_k_v
        return self
    
    def with_k_a(self, new_k_a: float) -> 'Slot0Configs':
        """
        Modifies this configuration's k_a parameter and returns itself for
        method-chaining and easier to use config API.
    
        Acceleration Feedforward Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the requested acceleration, the units should be
        defined as units of output per unit of requested input acceleration.
        For example, when controlling velocity using a duty cycle closed loop,
        the units for the acceleration feedfoward gain will be duty cycle per
        requested rps/s, or 1/(rps/s).
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
    
        :param new_k_a: Parameter to modify
        :type new_k_a: float
        :returns: Itself
        :rtype: Slot0Configs
        """
        self.k_a = new_k_a
        return self
    
    def with_k_g(self, new_k_g: float) -> 'Slot0Configs':
        """
        Modifies this configuration's k_g parameter and returns itself for
        method-chaining and easier to use config API.
    
        Gravity Feedforward/Feedback Gain
        
        This is added to the closed loop output. The sign is determined by
        GravityType. The unit for this constant is dependent on the control
        mode, typically fractional duty cycle, voltage, or torque current.
        
            - Minimum Value: -512
            - Maximum Value: 511
            - Default Value: 0
            - Units: 
    
        :param new_k_g: Parameter to modify
        :type new_k_g: float
        :returns: Itself
        :rtype: Slot0Configs
        """
        self.k_g = new_k_g
        return self
    
    def with_gravity_type(self, new_gravity_type: GravityTypeValue) -> 'Slot0Configs':
        """
        Modifies this configuration's gravity_type parameter and returns itself for
        method-chaining and easier to use config API.
    
        Gravity Feedforward/Feedback Type
        
        This determines the type of the gravity feedforward/feedback.
        
        Choose Elevator_Static for systems where the gravity feedforward is
        constant, such as an elevator. The gravity feedforward output will
        always have the same sign.
        
        Choose Arm_Cosine for systems where the gravity feedback is dependent
        on the angular position of the mechanism, such as an arm. The gravity
        feedback output will vary depending on the mechanism angular position.
        Note that the sensor offset and ratios must be configured so that the
        sensor reports a position of 0 when the mechanism is horizonal
        (parallel to the ground), and the reported sensor position is 1:1 with
        the mechanism.
        
    
        :param new_gravity_type: Parameter to modify
        :type new_gravity_type: GravityTypeValue
        :returns: Itself
        :rtype: Slot0Configs
        """
        self.gravity_type = new_gravity_type
        return self
    
    def with_static_feedforward_sign(self, new_static_feedforward_sign: StaticFeedforwardSignValue) -> 'Slot0Configs':
        """
        Modifies this configuration's static_feedforward_sign parameter and returns itself for
        method-chaining and easier to use config API.
    
        Static Feedforward Sign during position closed loop
        
        This determines the sign of the applied kS during position closed-loop
        modes. The default behavior uses the velocity reference sign. This
        works well with velocity closed loop, Motion Magic® controls, and
        position closed loop when velocity reference is specified (motion
        profiling).
        
        However, when using position closed loop with zero velocity reference
        (no motion profiling), the application may want to apply static
        feedforward based on the closed loop error sign instead. When doing
        so, we recommend the minimal amount of kS, otherwise the motor output
        may dither when closed loop error is near zero.
        
    
        :param new_static_feedforward_sign: Parameter to modify
        :type new_static_feedforward_sign: StaticFeedforwardSignValue
        :returns: Itself
        :rtype: Slot0Configs
        """
        self.static_feedforward_sign = new_static_feedforward_sign
        return self
    

    @classmethod
    def from_other(clazz, value) -> "Slot0Configs":
        tmp = clazz()
        tmp.k_p = value.k_p
        tmp.k_i = value.k_i
        tmp.k_d = value.k_d
        tmp.k_s = value.k_s
        tmp.k_v = value.k_v
        tmp.k_a = value.k_a
        tmp.k_g = value.k_g
        tmp.gravity_type = value.gravity_type
        tmp.static_feedforward_sign = value.static_feedforward_sign
        return tmp
        

    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: Slot0")
        ss.append("Name: \"kP\" Value: \"" + str(self.k_p) + "\"")
        ss.append("Name: \"kI\" Value: \"" + str(self.k_i) + "\"")
        ss.append("Name: \"kD\" Value: \"" + str(self.k_d) + "\"")
        ss.append("Name: \"kS\" Value: \"" + str(self.k_s) + "\"")
        ss.append("Name: \"kV\" Value: \"" + str(self.k_v) + "\"")
        ss.append("Name: \"kA\" Value: \"" + str(self.k_a) + "\"")
        ss.append("Name: \"kG\" Value: \"" + str(self.k_g) + "\"")
        ss.append("Name: \"GravityType\" Value: \"" + str(self.gravity_type) + "\"")
        ss.append("Name: \"StaticFeedforwardSign\" Value: \"" + str(self.static_feedforward_sign) + "\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.SLOT0_KP.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_p = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.SLOT0_KI.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_i = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.SLOT0_KD.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_d = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.SLOT0_KS.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_s = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.SLOT0_KV.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_v = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.SLOT0_KA.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_a = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.SLOT0_KG.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_g = value.value
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.SLOT0_KG_TYPE.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.gravity_type = GravityTypeValue(value.value)
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.SLOT0_KS_SIGN.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.static_feedforward_sign = StaticFeedforwardSignValue(value.value)
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SLOT0_KP.value, self.k_p, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SLOT0_KI.value, self.k_i, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SLOT0_KD.value, self.k_d, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SLOT0_KS.value, self.k_s, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SLOT0_KV.value, self.k_v, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SLOT0_KA.value, self.k_a, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SLOT0_KG.value, self.k_g, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.SLOT0_KG_TYPE.value, self.gravity_type.value, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.SLOT0_KS_SIGN.value, self.static_feedforward_sign.value, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)


class Slot1Configs:
    """
    Gains for the specified slot.
    
    If this slot is selected, these gains are used in closed loop control
    requests.
    """

    def __init__(self):
        self.k_p: float = 0
        """
        Proportional Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by error in the input, the units should be defined
        as units of output per unit of input error. For example, when
        controlling velocity using a duty cycle closed loop, the units for the
        proportional gain will be duty cycle per rps, or 1/rps.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
        """
        self.k_i: float = 0
        """
        Integral Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by error in the input integrated over time (in
        units of seconds), the units should be defined as units of output per
        unit of integrated input error. For example, when controlling velocity
        using a duty cycle closed loop, integrating velocity over time results
        in rps * s = rotations. Therefore, the units for the integral gain
        will be duty cycle per rotation of accumulated error, or 1/rot.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
        """
        self.k_d: float = 0
        """
        Derivative Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the derivative of error in the input with
        respect to time (in units of seconds), the units should be defined as
        units of output per unit of the differentiated input error. For
        example, when controlling velocity using a duty cycle closed loop, the
        derivative of velocity with respect to time is rps/s, which is
        acceleration. Therefore, the units for the derivative gain will be
        duty cycle per unit of acceleration error, or 1/(rps/s).
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
        """
        self.k_s: float = 0
        """
        Static Feedforward Gain
        
        This is added to the closed loop output. The unit for this constant is
        dependent on the control mode, typically fractional duty cycle,
        voltage, or torque current.
        
        The sign is typically determined by reference velocity when using
        position, velocity, and Motion Magic® closed loop modes. However, when
        using position closed loop with zero velocity reference (no motion
        profiling), the application can instead use the position closed loop
        error by setting the Static Feedforward Sign configuration parameter. 
        When doing so, we recommend the minimal amount of kS, otherwise the
        motor output may dither when closed loop error is near zero.
        
            - Minimum Value: -512
            - Maximum Value: 511
            - Default Value: 0
            - Units: 
        """
        self.k_v: float = 0
        """
        Velocity Feedforward Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the requested velocity, the units should be
        defined as units of output per unit of requested input velocity. For
        example, when controlling velocity using a duty cycle closed loop, the
        units for the velocity feedfoward gain will be duty cycle per
        requested rps, or 1/rps.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
        """
        self.k_a: float = 0
        """
        Acceleration Feedforward Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the requested acceleration, the units should be
        defined as units of output per unit of requested input acceleration.
        For example, when controlling velocity using a duty cycle closed loop,
        the units for the acceleration feedfoward gain will be duty cycle per
        requested rps/s, or 1/(rps/s).
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
        """
        self.k_g: float = 0
        """
        Gravity Feedforward/Feedback Gain
        
        This is added to the closed loop output. The sign is determined by
        GravityType. The unit for this constant is dependent on the control
        mode, typically fractional duty cycle, voltage, or torque current.
        
            - Minimum Value: -512
            - Maximum Value: 511
            - Default Value: 0
            - Units: 
        """
        self.gravity_type: GravityTypeValue = GravityTypeValue.ELEVATOR_STATIC
        """
        Gravity Feedforward/Feedback Type
        
        This determines the type of the gravity feedforward/feedback.
        
        Choose Elevator_Static for systems where the gravity feedforward is
        constant, such as an elevator. The gravity feedforward output will
        always be positive.
        
        Choose Arm_Cosine for systems where the gravity feedback is dependent
        on the angular position of the mechanism, such as an arm. The gravity
        feedback output will vary depending on the mechanism angular position.
        Note that the sensor offset and ratios must be configured so that the
        sensor position is 0 when the mechanism is horizonal, and one rotation
        of the mechanism corresponds to one rotation of the sensor position.
        
        """
        self.static_feedforward_sign: StaticFeedforwardSignValue = StaticFeedforwardSignValue.USE_VELOCITY_SIGN
        """
        Static Feedforward Sign during position closed loop
        
        This determines the sign of the applied kS during position closed-loop
        modes. The default behavior uses the velocity reference sign. This
        works well with velocity closed loop, Motion Magic® controls, and
        position closed loop when velocity reference is specified (motion
        profiling).
        
        However, when using position closed loop with zero velocity reference
        (no motion profiling), the application may want to apply static
        feedforward based on the closed loop error sign instead. When doing
        so, we recommend the minimal amount of kS, otherwise the motor output
        may dither when closed loop error is near zero.
        
        """
    
    def with_k_p(self, new_k_p: float) -> 'Slot1Configs':
        """
        Modifies this configuration's k_p parameter and returns itself for
        method-chaining and easier to use config API.
    
        Proportional Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by error in the input, the units should be defined
        as units of output per unit of input error. For example, when
        controlling velocity using a duty cycle closed loop, the units for the
        proportional gain will be duty cycle per rps, or 1/rps.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
    
        :param new_k_p: Parameter to modify
        :type new_k_p: float
        :returns: Itself
        :rtype: Slot1Configs
        """
        self.k_p = new_k_p
        return self
    
    def with_k_i(self, new_k_i: float) -> 'Slot1Configs':
        """
        Modifies this configuration's k_i parameter and returns itself for
        method-chaining and easier to use config API.
    
        Integral Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by error in the input integrated over time (in
        units of seconds), the units should be defined as units of output per
        unit of integrated input error. For example, when controlling velocity
        using a duty cycle closed loop, integrating velocity over time results
        in rps * s = rotations. Therefore, the units for the integral gain
        will be duty cycle per rotation of accumulated error, or 1/rot.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
    
        :param new_k_i: Parameter to modify
        :type new_k_i: float
        :returns: Itself
        :rtype: Slot1Configs
        """
        self.k_i = new_k_i
        return self
    
    def with_k_d(self, new_k_d: float) -> 'Slot1Configs':
        """
        Modifies this configuration's k_d parameter and returns itself for
        method-chaining and easier to use config API.
    
        Derivative Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the derivative of error in the input with
        respect to time (in units of seconds), the units should be defined as
        units of output per unit of the differentiated input error. For
        example, when controlling velocity using a duty cycle closed loop, the
        derivative of velocity with respect to time is rps/s, which is
        acceleration. Therefore, the units for the derivative gain will be
        duty cycle per unit of acceleration error, or 1/(rps/s).
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
    
        :param new_k_d: Parameter to modify
        :type new_k_d: float
        :returns: Itself
        :rtype: Slot1Configs
        """
        self.k_d = new_k_d
        return self
    
    def with_k_s(self, new_k_s: float) -> 'Slot1Configs':
        """
        Modifies this configuration's k_s parameter and returns itself for
        method-chaining and easier to use config API.
    
        Static Feedforward Gain
        
        This is added to the closed loop output. The unit for this constant is
        dependent on the control mode, typically fractional duty cycle,
        voltage, or torque current.
        
        The sign is typically determined by reference velocity when using
        position, velocity, and Motion Magic® closed loop modes. However, when
        using position closed loop with zero velocity reference (no motion
        profiling), the application can instead use the position closed loop
        error by setting the Static Feedforward Sign configuration parameter. 
        When doing so, we recommend the minimal amount of kS, otherwise the
        motor output may dither when closed loop error is near zero.
        
            - Minimum Value: -512
            - Maximum Value: 511
            - Default Value: 0
            - Units: 
    
        :param new_k_s: Parameter to modify
        :type new_k_s: float
        :returns: Itself
        :rtype: Slot1Configs
        """
        self.k_s = new_k_s
        return self
    
    def with_k_v(self, new_k_v: float) -> 'Slot1Configs':
        """
        Modifies this configuration's k_v parameter and returns itself for
        method-chaining and easier to use config API.
    
        Velocity Feedforward Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the requested velocity, the units should be
        defined as units of output per unit of requested input velocity. For
        example, when controlling velocity using a duty cycle closed loop, the
        units for the velocity feedfoward gain will be duty cycle per
        requested rps, or 1/rps.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
    
        :param new_k_v: Parameter to modify
        :type new_k_v: float
        :returns: Itself
        :rtype: Slot1Configs
        """
        self.k_v = new_k_v
        return self
    
    def with_k_a(self, new_k_a: float) -> 'Slot1Configs':
        """
        Modifies this configuration's k_a parameter and returns itself for
        method-chaining and easier to use config API.
    
        Acceleration Feedforward Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the requested acceleration, the units should be
        defined as units of output per unit of requested input acceleration.
        For example, when controlling velocity using a duty cycle closed loop,
        the units for the acceleration feedfoward gain will be duty cycle per
        requested rps/s, or 1/(rps/s).
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
    
        :param new_k_a: Parameter to modify
        :type new_k_a: float
        :returns: Itself
        :rtype: Slot1Configs
        """
        self.k_a = new_k_a
        return self
    
    def with_k_g(self, new_k_g: float) -> 'Slot1Configs':
        """
        Modifies this configuration's k_g parameter and returns itself for
        method-chaining and easier to use config API.
    
        Gravity Feedforward/Feedback Gain
        
        This is added to the closed loop output. The sign is determined by
        GravityType. The unit for this constant is dependent on the control
        mode, typically fractional duty cycle, voltage, or torque current.
        
            - Minimum Value: -512
            - Maximum Value: 511
            - Default Value: 0
            - Units: 
    
        :param new_k_g: Parameter to modify
        :type new_k_g: float
        :returns: Itself
        :rtype: Slot1Configs
        """
        self.k_g = new_k_g
        return self
    
    def with_gravity_type(self, new_gravity_type: GravityTypeValue) -> 'Slot1Configs':
        """
        Modifies this configuration's gravity_type parameter and returns itself for
        method-chaining and easier to use config API.
    
        Gravity Feedforward/Feedback Type
        
        This determines the type of the gravity feedforward/feedback.
        
        Choose Elevator_Static for systems where the gravity feedforward is
        constant, such as an elevator. The gravity feedforward output will
        always be positive.
        
        Choose Arm_Cosine for systems where the gravity feedback is dependent
        on the angular position of the mechanism, such as an arm. The gravity
        feedback output will vary depending on the mechanism angular position.
        Note that the sensor offset and ratios must be configured so that the
        sensor position is 0 when the mechanism is horizonal, and one rotation
        of the mechanism corresponds to one rotation of the sensor position.
        
    
        :param new_gravity_type: Parameter to modify
        :type new_gravity_type: GravityTypeValue
        :returns: Itself
        :rtype: Slot1Configs
        """
        self.gravity_type = new_gravity_type
        return self
    
    def with_static_feedforward_sign(self, new_static_feedforward_sign: StaticFeedforwardSignValue) -> 'Slot1Configs':
        """
        Modifies this configuration's static_feedforward_sign parameter and returns itself for
        method-chaining and easier to use config API.
    
        Static Feedforward Sign during position closed loop
        
        This determines the sign of the applied kS during position closed-loop
        modes. The default behavior uses the velocity reference sign. This
        works well with velocity closed loop, Motion Magic® controls, and
        position closed loop when velocity reference is specified (motion
        profiling).
        
        However, when using position closed loop with zero velocity reference
        (no motion profiling), the application may want to apply static
        feedforward based on the closed loop error sign instead. When doing
        so, we recommend the minimal amount of kS, otherwise the motor output
        may dither when closed loop error is near zero.
        
    
        :param new_static_feedforward_sign: Parameter to modify
        :type new_static_feedforward_sign: StaticFeedforwardSignValue
        :returns: Itself
        :rtype: Slot1Configs
        """
        self.static_feedforward_sign = new_static_feedforward_sign
        return self
    

    @classmethod
    def from_other(clazz, value) -> "Slot1Configs":
        tmp = clazz()
        tmp.k_p = value.k_p
        tmp.k_i = value.k_i
        tmp.k_d = value.k_d
        tmp.k_s = value.k_s
        tmp.k_v = value.k_v
        tmp.k_a = value.k_a
        tmp.k_g = value.k_g
        tmp.gravity_type = value.gravity_type
        tmp.static_feedforward_sign = value.static_feedforward_sign
        return tmp
        

    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: Slot1")
        ss.append("Name: \"kP\" Value: \"" + str(self.k_p) + "\"")
        ss.append("Name: \"kI\" Value: \"" + str(self.k_i) + "\"")
        ss.append("Name: \"kD\" Value: \"" + str(self.k_d) + "\"")
        ss.append("Name: \"kS\" Value: \"" + str(self.k_s) + "\"")
        ss.append("Name: \"kV\" Value: \"" + str(self.k_v) + "\"")
        ss.append("Name: \"kA\" Value: \"" + str(self.k_a) + "\"")
        ss.append("Name: \"kG\" Value: \"" + str(self.k_g) + "\"")
        ss.append("Name: \"GravityType\" Value: \"" + str(self.gravity_type) + "\"")
        ss.append("Name: \"StaticFeedforwardSign\" Value: \"" + str(self.static_feedforward_sign) + "\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.SLOT1_KP.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_p = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.SLOT1_KI.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_i = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.SLOT1_KD.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_d = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.SLOT1_KS.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_s = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.SLOT1_KV.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_v = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.SLOT1_KA.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_a = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.SLOT1_KG.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_g = value.value
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.SLOT1_KG_TYPE.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.gravity_type = GravityTypeValue(value.value)
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.SLOT1_KS_SIGN.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.static_feedforward_sign = StaticFeedforwardSignValue(value.value)
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SLOT1_KP.value, self.k_p, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SLOT1_KI.value, self.k_i, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SLOT1_KD.value, self.k_d, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SLOT1_KS.value, self.k_s, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SLOT1_KV.value, self.k_v, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SLOT1_KA.value, self.k_a, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SLOT1_KG.value, self.k_g, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.SLOT1_KG_TYPE.value, self.gravity_type.value, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.SLOT1_KS_SIGN.value, self.static_feedforward_sign.value, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)


class Slot2Configs:
    """
    Gains for the specified slot.
    
    If this slot is selected, these gains are used in closed loop control
    requests.
    """

    def __init__(self):
        self.k_p: float = 0
        """
        Proportional Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by error in the input, the units should be defined
        as units of output per unit of input error. For example, when
        controlling velocity using a duty cycle closed loop, the units for the
        proportional gain will be duty cycle per rps, or 1/rps.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
        """
        self.k_i: float = 0
        """
        Integral Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by error in the input integrated over time (in
        units of seconds), the units should be defined as units of output per
        unit of integrated input error. For example, when controlling velocity
        using a duty cycle closed loop, integrating velocity over time results
        in rps * s = rotations. Therefore, the units for the integral gain
        will be duty cycle per rotation of accumulated error, or 1/rot.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
        """
        self.k_d: float = 0
        """
        Derivative Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the derivative of error in the input with
        respect to time (in units of seconds), the units should be defined as
        units of output per unit of the differentiated input error. For
        example, when controlling velocity using a duty cycle closed loop, the
        derivative of velocity with respect to time is rps/s, which is
        acceleration. Therefore, the units for the derivative gain will be
        duty cycle per unit of acceleration error, or 1/(rps/s).
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
        """
        self.k_s: float = 0
        """
        Static Feedforward Gain
        
        This is added to the closed loop output. The unit for this constant is
        dependent on the control mode, typically fractional duty cycle,
        voltage, or torque current.
        
        The sign is typically determined by reference velocity when using
        position, velocity, and Motion Magic® closed loop modes. However, when
        using position closed loop with zero velocity reference (no motion
        profiling), the application can instead use the position closed loop
        error by setting the Static Feedforward Sign configuration parameter. 
        When doing so, we recommend the minimal amount of kS, otherwise the
        motor output may dither when closed loop error is near zero.
        
            - Minimum Value: -512
            - Maximum Value: 511
            - Default Value: 0
            - Units: 
        """
        self.k_v: float = 0
        """
        Velocity Feedforward Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the requested velocity, the units should be
        defined as units of output per unit of requested input velocity. For
        example, when controlling velocity using a duty cycle closed loop, the
        units for the velocity feedfoward gain will be duty cycle per
        requested rps, or 1/rps.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
        """
        self.k_a: float = 0
        """
        Acceleration Feedforward Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the requested acceleration, the units should be
        defined as units of output per unit of requested input acceleration.
        For example, when controlling velocity using a duty cycle closed loop,
        the units for the acceleration feedfoward gain will be duty cycle per
        requested rps/s, or 1/(rps/s).
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
        """
        self.k_g: float = 0
        """
        Gravity Feedforward/Feedback Gain
        
        This is added to the closed loop output. The sign is determined by
        GravityType. The unit for this constant is dependent on the control
        mode, typically fractional duty cycle, voltage, or torque current.
        
            - Minimum Value: -512
            - Maximum Value: 511
            - Default Value: 0
            - Units: 
        """
        self.gravity_type: GravityTypeValue = GravityTypeValue.ELEVATOR_STATIC
        """
        Gravity Feedforward/Feedback Type
        
        This determines the type of the gravity feedforward/feedback.
        
        Choose Elevator_Static for systems where the gravity feedforward is
        constant, such as an elevator. The gravity feedforward output will
        always be positive.
        
        Choose Arm_Cosine for systems where the gravity feedback is dependent
        on the angular position of the mechanism, such as an arm. The gravity
        feedback output will vary depending on the mechanism angular position.
        Note that the sensor offset and ratios must be configured so that the
        sensor position is 0 when the mechanism is horizonal, and one rotation
        of the mechanism corresponds to one rotation of the sensor position.
        
        """
        self.static_feedforward_sign: StaticFeedforwardSignValue = StaticFeedforwardSignValue.USE_VELOCITY_SIGN
        """
        Static Feedforward Sign during position closed loop
        
        This determines the sign of the applied kS during position closed-loop
        modes. The default behavior uses the velocity reference sign. This
        works well with velocity closed loop, Motion Magic® controls, and
        position closed loop when velocity reference is specified (motion
        profiling).
        
        However, when using position closed loop with zero velocity reference
        (no motion profiling), the application may want to apply static
        feedforward based on the closed loop error sign instead. When doing
        so, we recommend the minimal amount of kS, otherwise the motor output
        may dither when closed loop error is near zero.
        
        """
    
    def with_k_p(self, new_k_p: float) -> 'Slot2Configs':
        """
        Modifies this configuration's k_p parameter and returns itself for
        method-chaining and easier to use config API.
    
        Proportional Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by error in the input, the units should be defined
        as units of output per unit of input error. For example, when
        controlling velocity using a duty cycle closed loop, the units for the
        proportional gain will be duty cycle per rps, or 1/rps.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
    
        :param new_k_p: Parameter to modify
        :type new_k_p: float
        :returns: Itself
        :rtype: Slot2Configs
        """
        self.k_p = new_k_p
        return self
    
    def with_k_i(self, new_k_i: float) -> 'Slot2Configs':
        """
        Modifies this configuration's k_i parameter and returns itself for
        method-chaining and easier to use config API.
    
        Integral Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by error in the input integrated over time (in
        units of seconds), the units should be defined as units of output per
        unit of integrated input error. For example, when controlling velocity
        using a duty cycle closed loop, integrating velocity over time results
        in rps * s = rotations. Therefore, the units for the integral gain
        will be duty cycle per rotation of accumulated error, or 1/rot.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
    
        :param new_k_i: Parameter to modify
        :type new_k_i: float
        :returns: Itself
        :rtype: Slot2Configs
        """
        self.k_i = new_k_i
        return self
    
    def with_k_d(self, new_k_d: float) -> 'Slot2Configs':
        """
        Modifies this configuration's k_d parameter and returns itself for
        method-chaining and easier to use config API.
    
        Derivative Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the derivative of error in the input with
        respect to time (in units of seconds), the units should be defined as
        units of output per unit of the differentiated input error. For
        example, when controlling velocity using a duty cycle closed loop, the
        derivative of velocity with respect to time is rps/s, which is
        acceleration. Therefore, the units for the derivative gain will be
        duty cycle per unit of acceleration error, or 1/(rps/s).
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
    
        :param new_k_d: Parameter to modify
        :type new_k_d: float
        :returns: Itself
        :rtype: Slot2Configs
        """
        self.k_d = new_k_d
        return self
    
    def with_k_s(self, new_k_s: float) -> 'Slot2Configs':
        """
        Modifies this configuration's k_s parameter and returns itself for
        method-chaining and easier to use config API.
    
        Static Feedforward Gain
        
        This is added to the closed loop output. The unit for this constant is
        dependent on the control mode, typically fractional duty cycle,
        voltage, or torque current.
        
        The sign is typically determined by reference velocity when using
        position, velocity, and Motion Magic® closed loop modes. However, when
        using position closed loop with zero velocity reference (no motion
        profiling), the application can instead use the position closed loop
        error by setting the Static Feedforward Sign configuration parameter. 
        When doing so, we recommend the minimal amount of kS, otherwise the
        motor output may dither when closed loop error is near zero.
        
            - Minimum Value: -512
            - Maximum Value: 511
            - Default Value: 0
            - Units: 
    
        :param new_k_s: Parameter to modify
        :type new_k_s: float
        :returns: Itself
        :rtype: Slot2Configs
        """
        self.k_s = new_k_s
        return self
    
    def with_k_v(self, new_k_v: float) -> 'Slot2Configs':
        """
        Modifies this configuration's k_v parameter and returns itself for
        method-chaining and easier to use config API.
    
        Velocity Feedforward Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the requested velocity, the units should be
        defined as units of output per unit of requested input velocity. For
        example, when controlling velocity using a duty cycle closed loop, the
        units for the velocity feedfoward gain will be duty cycle per
        requested rps, or 1/rps.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
    
        :param new_k_v: Parameter to modify
        :type new_k_v: float
        :returns: Itself
        :rtype: Slot2Configs
        """
        self.k_v = new_k_v
        return self
    
    def with_k_a(self, new_k_a: float) -> 'Slot2Configs':
        """
        Modifies this configuration's k_a parameter and returns itself for
        method-chaining and easier to use config API.
    
        Acceleration Feedforward Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the requested acceleration, the units should be
        defined as units of output per unit of requested input acceleration.
        For example, when controlling velocity using a duty cycle closed loop,
        the units for the acceleration feedfoward gain will be duty cycle per
        requested rps/s, or 1/(rps/s).
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
    
        :param new_k_a: Parameter to modify
        :type new_k_a: float
        :returns: Itself
        :rtype: Slot2Configs
        """
        self.k_a = new_k_a
        return self
    
    def with_k_g(self, new_k_g: float) -> 'Slot2Configs':
        """
        Modifies this configuration's k_g parameter and returns itself for
        method-chaining and easier to use config API.
    
        Gravity Feedforward/Feedback Gain
        
        This is added to the closed loop output. The sign is determined by
        GravityType. The unit for this constant is dependent on the control
        mode, typically fractional duty cycle, voltage, or torque current.
        
            - Minimum Value: -512
            - Maximum Value: 511
            - Default Value: 0
            - Units: 
    
        :param new_k_g: Parameter to modify
        :type new_k_g: float
        :returns: Itself
        :rtype: Slot2Configs
        """
        self.k_g = new_k_g
        return self
    
    def with_gravity_type(self, new_gravity_type: GravityTypeValue) -> 'Slot2Configs':
        """
        Modifies this configuration's gravity_type parameter and returns itself for
        method-chaining and easier to use config API.
    
        Gravity Feedforward/Feedback Type
        
        This determines the type of the gravity feedforward/feedback.
        
        Choose Elevator_Static for systems where the gravity feedforward is
        constant, such as an elevator. The gravity feedforward output will
        always be positive.
        
        Choose Arm_Cosine for systems where the gravity feedback is dependent
        on the angular position of the mechanism, such as an arm. The gravity
        feedback output will vary depending on the mechanism angular position.
        Note that the sensor offset and ratios must be configured so that the
        sensor position is 0 when the mechanism is horizonal, and one rotation
        of the mechanism corresponds to one rotation of the sensor position.
        
    
        :param new_gravity_type: Parameter to modify
        :type new_gravity_type: GravityTypeValue
        :returns: Itself
        :rtype: Slot2Configs
        """
        self.gravity_type = new_gravity_type
        return self
    
    def with_static_feedforward_sign(self, new_static_feedforward_sign: StaticFeedforwardSignValue) -> 'Slot2Configs':
        """
        Modifies this configuration's static_feedforward_sign parameter and returns itself for
        method-chaining and easier to use config API.
    
        Static Feedforward Sign during position closed loop
        
        This determines the sign of the applied kS during position closed-loop
        modes. The default behavior uses the velocity reference sign. This
        works well with velocity closed loop, Motion Magic® controls, and
        position closed loop when velocity reference is specified (motion
        profiling).
        
        However, when using position closed loop with zero velocity reference
        (no motion profiling), the application may want to apply static
        feedforward based on the closed loop error sign instead. When doing
        so, we recommend the minimal amount of kS, otherwise the motor output
        may dither when closed loop error is near zero.
        
    
        :param new_static_feedforward_sign: Parameter to modify
        :type new_static_feedforward_sign: StaticFeedforwardSignValue
        :returns: Itself
        :rtype: Slot2Configs
        """
        self.static_feedforward_sign = new_static_feedforward_sign
        return self
    

    @classmethod
    def from_other(clazz, value) -> "Slot2Configs":
        tmp = clazz()
        tmp.k_p = value.k_p
        tmp.k_i = value.k_i
        tmp.k_d = value.k_d
        tmp.k_s = value.k_s
        tmp.k_v = value.k_v
        tmp.k_a = value.k_a
        tmp.k_g = value.k_g
        tmp.gravity_type = value.gravity_type
        tmp.static_feedforward_sign = value.static_feedforward_sign
        return tmp
        

    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: Slot2")
        ss.append("Name: \"kP\" Value: \"" + str(self.k_p) + "\"")
        ss.append("Name: \"kI\" Value: \"" + str(self.k_i) + "\"")
        ss.append("Name: \"kD\" Value: \"" + str(self.k_d) + "\"")
        ss.append("Name: \"kS\" Value: \"" + str(self.k_s) + "\"")
        ss.append("Name: \"kV\" Value: \"" + str(self.k_v) + "\"")
        ss.append("Name: \"kA\" Value: \"" + str(self.k_a) + "\"")
        ss.append("Name: \"kG\" Value: \"" + str(self.k_g) + "\"")
        ss.append("Name: \"GravityType\" Value: \"" + str(self.gravity_type) + "\"")
        ss.append("Name: \"StaticFeedforwardSign\" Value: \"" + str(self.static_feedforward_sign) + "\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.SLOT2_KP.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_p = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.SLOT2_KI.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_i = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.SLOT2_KD.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_d = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.SLOT2_KS.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_s = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.SLOT2_KV.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_v = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.SLOT2_KA.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_a = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(SpnValue.SLOT2_KG.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_g = value.value
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.SLOT2_KG_TYPE.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.gravity_type = GravityTypeValue(value.value)
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(SpnValue.SLOT2_KS_SIGN.value, ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.static_feedforward_sign = StaticFeedforwardSignValue(value.value)
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SLOT2_KP.value, self.k_p, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SLOT2_KI.value, self.k_i, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SLOT2_KD.value, self.k_d, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SLOT2_KS.value, self.k_s, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SLOT2_KV.value, self.k_v, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SLOT2_KA.value, self.k_a, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SLOT2_KG.value, self.k_g, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.SLOT2_KG_TYPE.value, self.gravity_type.value, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        Native.instance().c_ctre_phoenix6_serialize_int(SpnValue.SLOT2_KS_SIGN.value, self.static_feedforward_sign.value, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        return "".join(ss)



class SlotConfigs:
    """
    Gains for the specified slot.
    
    If this slot is selected, these gains are used in closed loop control
    requests.
    """

    def __init__(self):
        self.__generic_map: dict[int, dict[str, int]] = {
            0: {
                "kPSpn": SpnValue.SLOT0_KP.value,
                "kISpn": SpnValue.SLOT0_KI.value,
                "kDSpn": SpnValue.SLOT0_KD.value,
                "kSSpn": SpnValue.SLOT0_KS.value,
                "kVSpn": SpnValue.SLOT0_KV.value,
                "kASpn": SpnValue.SLOT0_KA.value,
                "kGSpn": SpnValue.SLOT0_KG.value,
                "GravityTypeSpn": SpnValue.SLOT0_KG_TYPE.value,
                "StaticFeedforwardSignSpn": SpnValue.SLOT0_KS_SIGN.value,
            },
            1: {
                "kPSpn": SpnValue.SLOT1_KP.value,
                "kISpn": SpnValue.SLOT1_KI.value,
                "kDSpn": SpnValue.SLOT1_KD.value,
                "kSSpn": SpnValue.SLOT1_KS.value,
                "kVSpn": SpnValue.SLOT1_KV.value,
                "kASpn": SpnValue.SLOT1_KA.value,
                "kGSpn": SpnValue.SLOT1_KG.value,
                "GravityTypeSpn": SpnValue.SLOT1_KG_TYPE.value,
                "StaticFeedforwardSignSpn": SpnValue.SLOT1_KS_SIGN.value,
            },
            2: {
                "kPSpn": SpnValue.SLOT2_KP.value,
                "kISpn": SpnValue.SLOT2_KI.value,
                "kDSpn": SpnValue.SLOT2_KD.value,
                "kSSpn": SpnValue.SLOT2_KS.value,
                "kVSpn": SpnValue.SLOT2_KV.value,
                "kASpn": SpnValue.SLOT2_KA.value,
                "kGSpn": SpnValue.SLOT2_KG.value,
                "GravityTypeSpn": SpnValue.SLOT2_KG_TYPE.value,
                "StaticFeedforwardSignSpn": SpnValue.SLOT2_KS_SIGN.value,
            },
        }
        self.slot_number = 0
        """
        Chooses which slot these configs are for.
        """
        self.k_p: float = 0
        """
        Proportional Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by error in the input, the units should be defined
        as units of output per unit of input error. For example, when
        controlling velocity using a duty cycle closed loop, the units for the
        proportional gain will be duty cycle per rps of error, or 1/rps.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
        """
        self.k_i: float = 0
        """
        Integral Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by error in the input integrated over time (in
        units of seconds), the units should be defined as units of output per
        unit of integrated input error. For example, when controlling velocity
        using a duty cycle closed loop, integrating velocity over time results
        in rps * s = rotations. Therefore, the units for the integral gain
        will be duty cycle per rotation of accumulated error, or 1/rot.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
        """
        self.k_d: float = 0
        """
        Derivative Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the derivative of error in the input with
        respect to time (in units of seconds), the units should be defined as
        units of output per unit of the differentiated input error. For
        example, when controlling velocity using a duty cycle closed loop, the
        derivative of velocity with respect to time is rps/s, which is
        acceleration. Therefore, the units for the derivative gain will be
        duty cycle per unit of acceleration error, or 1/(rps/s).
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
        """
        self.k_s: float = 0
        """
        Static Feedforward Gain
        
        This is added to the closed loop output. The unit for this constant is
        dependent on the control mode, typically fractional duty cycle,
        voltage, or torque current.
        
        The sign is typically determined by reference velocity when using
        position, velocity, and Motion Magic® closed loop modes. However, when
        using position closed loop with zero velocity reference (no motion
        profiling), the application can instead use the position closed loop
        error by setting the Static Feedforward Sign configuration parameter. 
        When doing so, we recommend the minimal amount of kS, otherwise the
        motor output may dither when closed loop error is near zero.
        
            - Minimum Value: -512
            - Maximum Value: 511
            - Default Value: 0
            - Units: 
        """
        self.k_v: float = 0
        """
        Velocity Feedforward Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the requested velocity, the units should be
        defined as units of output per unit of requested input velocity. For
        example, when controlling velocity using a duty cycle closed loop, the
        units for the velocity feedfoward gain will be duty cycle per
        requested rps, or 1/rps.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
        """
        self.k_a: float = 0
        """
        Acceleration Feedforward Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the requested acceleration, the units should be
        defined as units of output per unit of requested input acceleration.
        For example, when controlling velocity using a duty cycle closed loop,
        the units for the acceleration feedfoward gain will be duty cycle per
        requested rps/s, or 1/(rps/s).
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
        """
        self.k_g: float = 0
        """
        Gravity Feedforward/Feedback Gain
        
        This is added to the closed loop output. The sign is determined by
        GravityType. The unit for this constant is dependent on the control
        mode, typically fractional duty cycle, voltage, or torque current.
        
            - Minimum Value: -512
            - Maximum Value: 511
            - Default Value: 0
            - Units: 
        """
        self.gravity_type: GravityTypeValue = GravityTypeValue.ELEVATOR_STATIC
        """
        Gravity Feedforward/Feedback Type
        
        This determines the type of the gravity feedforward/feedback.
        
        Choose Elevator_Static for systems where the gravity feedforward is
        constant, such as an elevator. The gravity feedforward output will
        always have the same sign.
        
        Choose Arm_Cosine for systems where the gravity feedback is dependent
        on the angular position of the mechanism, such as an arm. The gravity
        feedback output will vary depending on the mechanism angular position.
        Note that the sensor offset and ratios must be configured so that the
        sensor reports a position of 0 when the mechanism is horizonal
        (parallel to the ground), and the reported sensor position is 1:1 with
        the mechanism.
        
        """
        self.static_feedforward_sign: StaticFeedforwardSignValue = StaticFeedforwardSignValue.USE_VELOCITY_SIGN
        """
        Static Feedforward Sign during position closed loop
        
        This determines the sign of the applied kS during position closed-loop
        modes. The default behavior uses the velocity reference sign. This
        works well with velocity closed loop, Motion Magic® controls, and
        position closed loop when velocity reference is specified (motion
        profiling).
        
        However, when using position closed loop with zero velocity reference
        (no motion profiling), the application may want to apply static
        feedforward based on the closed loop error sign instead. When doing
        so, we recommend the minimal amount of kS, otherwise the motor output
        may dither when closed loop error is near zero.
        
        """
    
    def with_k_p(self, new_k_p: float) -> 'SlotConfigs':
        """
        Modifies this configuration's k_p parameter and returns itself for
        method-chaining and easier to use config API.
    
        Proportional Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by error in the input, the units should be defined
        as units of output per unit of input error. For example, when
        controlling velocity using a duty cycle closed loop, the units for the
        proportional gain will be duty cycle per rps of error, or 1/rps.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
    
        :param new_k_p: Parameter to modify
        :type new_k_p: float
        :returns: Itself
        :rtype: SlotConfigs
        """
        self.k_p = new_k_p
        return self
    
    def with_k_i(self, new_k_i: float) -> 'SlotConfigs':
        """
        Modifies this configuration's k_i parameter and returns itself for
        method-chaining and easier to use config API.
    
        Integral Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by error in the input integrated over time (in
        units of seconds), the units should be defined as units of output per
        unit of integrated input error. For example, when controlling velocity
        using a duty cycle closed loop, integrating velocity over time results
        in rps * s = rotations. Therefore, the units for the integral gain
        will be duty cycle per rotation of accumulated error, or 1/rot.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
    
        :param new_k_i: Parameter to modify
        :type new_k_i: float
        :returns: Itself
        :rtype: SlotConfigs
        """
        self.k_i = new_k_i
        return self
    
    def with_k_d(self, new_k_d: float) -> 'SlotConfigs':
        """
        Modifies this configuration's k_d parameter and returns itself for
        method-chaining and easier to use config API.
    
        Derivative Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the derivative of error in the input with
        respect to time (in units of seconds), the units should be defined as
        units of output per unit of the differentiated input error. For
        example, when controlling velocity using a duty cycle closed loop, the
        derivative of velocity with respect to time is rps/s, which is
        acceleration. Therefore, the units for the derivative gain will be
        duty cycle per unit of acceleration error, or 1/(rps/s).
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
    
        :param new_k_d: Parameter to modify
        :type new_k_d: float
        :returns: Itself
        :rtype: SlotConfigs
        """
        self.k_d = new_k_d
        return self
    
    def with_k_s(self, new_k_s: float) -> 'SlotConfigs':
        """
        Modifies this configuration's k_s parameter and returns itself for
        method-chaining and easier to use config API.
    
        Static Feedforward Gain
        
        This is added to the closed loop output. The unit for this constant is
        dependent on the control mode, typically fractional duty cycle,
        voltage, or torque current.
        
        The sign is typically determined by reference velocity when using
        position, velocity, and Motion Magic® closed loop modes. However, when
        using position closed loop with zero velocity reference (no motion
        profiling), the application can instead use the position closed loop
        error by setting the Static Feedforward Sign configuration parameter. 
        When doing so, we recommend the minimal amount of kS, otherwise the
        motor output may dither when closed loop error is near zero.
        
            - Minimum Value: -512
            - Maximum Value: 511
            - Default Value: 0
            - Units: 
    
        :param new_k_s: Parameter to modify
        :type new_k_s: float
        :returns: Itself
        :rtype: SlotConfigs
        """
        self.k_s = new_k_s
        return self
    
    def with_k_v(self, new_k_v: float) -> 'SlotConfigs':
        """
        Modifies this configuration's k_v parameter and returns itself for
        method-chaining and easier to use config API.
    
        Velocity Feedforward Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the requested velocity, the units should be
        defined as units of output per unit of requested input velocity. For
        example, when controlling velocity using a duty cycle closed loop, the
        units for the velocity feedfoward gain will be duty cycle per
        requested rps, or 1/rps.
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
    
        :param new_k_v: Parameter to modify
        :type new_k_v: float
        :returns: Itself
        :rtype: SlotConfigs
        """
        self.k_v = new_k_v
        return self
    
    def with_k_a(self, new_k_a: float) -> 'SlotConfigs':
        """
        Modifies this configuration's k_a parameter and returns itself for
        method-chaining and easier to use config API.
    
        Acceleration Feedforward Gain
        
        The units for this gain is dependent on the control mode. Since this
        gain is multiplied by the requested acceleration, the units should be
        defined as units of output per unit of requested input acceleration.
        For example, when controlling velocity using a duty cycle closed loop,
        the units for the acceleration feedfoward gain will be duty cycle per
        requested rps/s, or 1/(rps/s).
        
            - Minimum Value: 0
            - Maximum Value: 3.4e+38
            - Default Value: 0
            - Units: 
    
        :param new_k_a: Parameter to modify
        :type new_k_a: float
        :returns: Itself
        :rtype: SlotConfigs
        """
        self.k_a = new_k_a
        return self
    
    def with_k_g(self, new_k_g: float) -> 'SlotConfigs':
        """
        Modifies this configuration's k_g parameter and returns itself for
        method-chaining and easier to use config API.
    
        Gravity Feedforward/Feedback Gain
        
        This is added to the closed loop output. The sign is determined by
        GravityType. The unit for this constant is dependent on the control
        mode, typically fractional duty cycle, voltage, or torque current.
        
            - Minimum Value: -512
            - Maximum Value: 511
            - Default Value: 0
            - Units: 
    
        :param new_k_g: Parameter to modify
        :type new_k_g: float
        :returns: Itself
        :rtype: SlotConfigs
        """
        self.k_g = new_k_g
        return self
    
    def with_gravity_type(self, new_gravity_type: GravityTypeValue) -> 'SlotConfigs':
        """
        Modifies this configuration's gravity_type parameter and returns itself for
        method-chaining and easier to use config API.
    
        Gravity Feedforward/Feedback Type
        
        This determines the type of the gravity feedforward/feedback.
        
        Choose Elevator_Static for systems where the gravity feedforward is
        constant, such as an elevator. The gravity feedforward output will
        always have the same sign.
        
        Choose Arm_Cosine for systems where the gravity feedback is dependent
        on the angular position of the mechanism, such as an arm. The gravity
        feedback output will vary depending on the mechanism angular position.
        Note that the sensor offset and ratios must be configured so that the
        sensor reports a position of 0 when the mechanism is horizonal
        (parallel to the ground), and the reported sensor position is 1:1 with
        the mechanism.
        
    
        :param new_gravity_type: Parameter to modify
        :type new_gravity_type: GravityTypeValue
        :returns: Itself
        :rtype: SlotConfigs
        """
        self.gravity_type = new_gravity_type
        return self
    
    def with_static_feedforward_sign(self, new_static_feedforward_sign: StaticFeedforwardSignValue) -> 'SlotConfigs':
        """
        Modifies this configuration's static_feedforward_sign parameter and returns itself for
        method-chaining and easier to use config API.
    
        Static Feedforward Sign during position closed loop
        
        This determines the sign of the applied kS during position closed-loop
        modes. The default behavior uses the velocity reference sign. This
        works well with velocity closed loop, Motion Magic® controls, and
        position closed loop when velocity reference is specified (motion
        profiling).
        
        However, when using position closed loop with zero velocity reference
        (no motion profiling), the application may want to apply static
        feedforward based on the closed loop error sign instead. When doing
        so, we recommend the minimal amount of kS, otherwise the motor output
        may dither when closed loop error is near zero.
        
    
        :param new_static_feedforward_sign: Parameter to modify
        :type new_static_feedforward_sign: StaticFeedforwardSignValue
        :returns: Itself
        :rtype: SlotConfigs
        """
        self.static_feedforward_sign = new_static_feedforward_sign
        return self
    


    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation
        :rtype: str
        """
        ss = []
        ss.append("Config Group: Slot")
        ss.append("Name: \"kP\" Value: \"" + str(self.k_p) + "\"")
        ss.append("Name: \"kI\" Value: \"" + str(self.k_i) + "\"")
        ss.append("Name: \"kD\" Value: \"" + str(self.k_d) + "\"")
        ss.append("Name: \"kS\" Value: \"" + str(self.k_s) + "\"")
        ss.append("Name: \"kV\" Value: \"" + str(self.k_v) + "\"")
        ss.append("Name: \"kA\" Value: \"" + str(self.k_a) + "\"")
        ss.append("Name: \"kG\" Value: \"" + str(self.k_g) + "\"")
        ss.append("Name: \"GravityType\" Value: \"" + str(self.gravity_type) + "\"")
        ss.append("Name: \"StaticFeedforwardSign\" Value: \"" + str(self.static_feedforward_sign) + "\"")
        return "\n".join(ss)

    def deserialize(self, string: str) -> StatusCode:
        """
        Deserialize string and put values into this object

        :param string: String to deserialize
        :type string: str
        :return: OK if deserialization is OK
        :rtype: StatusCode
        """
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(self.__generic_map[self.slot_number]["kPSpn"], ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_p = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(self.__generic_map[self.slot_number]["kISpn"], ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_i = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(self.__generic_map[self.slot_number]["kDSpn"], ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_d = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(self.__generic_map[self.slot_number]["kSSpn"], ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_s = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(self.__generic_map[self.slot_number]["kVSpn"], ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_v = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(self.__generic_map[self.slot_number]["kASpn"], ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_a = value.value
        value = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_deserialize_double(self.__generic_map[self.slot_number]["kGSpn"], ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.k_g = value.value
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(self.__generic_map[self.slot_number]["GravityTypeSpn"], ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.gravity_type = GravityTypeValue(value.value)
        value = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_deserialize_int(self.__generic_map[self.slot_number]["StaticFeedforwardSignSpn"], ctypes.c_char_p(bytes(string, encoding='utf-8')), len(string), ctypes.byref(value))
        self.static_feedforward_sign = StaticFeedforwardSignValue(value.value)
        return  StatusCode.OK

    def serialize(self) -> str:
        """
        Serialize this object into a string

        :return: This object's data serialized into a string
        :rtype: str
        """
        ss = []
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(self.__generic_map[self.slot_number]["kPSpn"], self.k_p, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        
        Native.instance().c_ctre_phoenix6_serialize_double(self.__generic_map[self.slot_number]["kISpn"], self.k_i, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        
        Native.instance().c_ctre_phoenix6_serialize_double(self.__generic_map[self.slot_number]["kDSpn"], self.k_d, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        
        Native.instance().c_ctre_phoenix6_serialize_double(self.__generic_map[self.slot_number]["kSSpn"], self.k_s, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        
        Native.instance().c_ctre_phoenix6_serialize_double(self.__generic_map[self.slot_number]["kVSpn"], self.k_v, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        
        Native.instance().c_ctre_phoenix6_serialize_double(self.__generic_map[self.slot_number]["kASpn"], self.k_a, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        
        Native.instance().c_ctre_phoenix6_serialize_double(self.__generic_map[self.slot_number]["kGSpn"], self.k_g, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        
        Native.instance().c_ctre_phoenix6_serialize_int(self.__generic_map[self.slot_number]["GravityTypeSpn"], self.gravity_type.value, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        
        Native.instance().c_ctre_phoenix6_serialize_int(self.__generic_map[self.slot_number]["StaticFeedforwardSignSpn"], self.static_feedforward_sign.value, ctypes.byref(value))
        if value.value is not None:
            ss.append(str(value.value, encoding='utf-8'))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        
        return "".join(ss)

    @classmethod
    def from_other(clazz, value) -> "SlotConfigs":
        tmp = clazz()
        
        if isinstance(value, Slot0Configs):
            tmp.k_p = value.k_p
            tmp.k_i = value.k_i
            tmp.k_d = value.k_d
            tmp.k_s = value.k_s
            tmp.k_v = value.k_v
            tmp.k_a = value.k_a
            tmp.k_g = value.k_g
            tmp.gravity_type = value.gravity_type
            tmp.static_feedforward_sign = value.static_feedforward_sign
            tmp.slot_number = 0
        
        if isinstance(value, Slot1Configs):
            tmp.k_p = value.k_p
            tmp.k_i = value.k_i
            tmp.k_d = value.k_d
            tmp.k_s = value.k_s
            tmp.k_v = value.k_v
            tmp.k_a = value.k_a
            tmp.k_g = value.k_g
            tmp.gravity_type = value.gravity_type
            tmp.static_feedforward_sign = value.static_feedforward_sign
            tmp.slot_number = 1
        
        if isinstance(value, Slot2Configs):
            tmp.k_p = value.k_p
            tmp.k_i = value.k_i
            tmp.k_d = value.k_d
            tmp.k_s = value.k_s
            tmp.k_v = value.k_v
            tmp.k_a = value.k_a
            tmp.k_g = value.k_g
            tmp.gravity_type = value.gravity_type
            tmp.static_feedforward_sign = value.static_feedforward_sign
            tmp.slot_number = 2
        return tmp

