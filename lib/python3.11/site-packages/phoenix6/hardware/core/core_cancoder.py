"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.hardware.parent_device import ParentDevice, SupportsSendRequest
from phoenix6.spns.spn_value import SpnValue
from phoenix6.status_code import StatusCode
from phoenix6.status_signal import *
from phoenix6.units import *
from phoenix6.sim.device_type import DeviceType
from phoenix6.configs.cancoder_configs import CANcoderConfigurator
from phoenix6.signals.spn_enums import MagnetHealthValue
from phoenix6.sim.cancoder_sim_state import CANcoderSimState

class CoreCANcoder(ParentDevice):
    """
    Constructs a new CANcoder object.

    :param device_id: ID of the device, as configured in Phoenix Tuner.
    :type device_id: int
    :param canbus: Name of the CAN bus this device is on. Possible CAN bus strings are:

        - "rio" for the native roboRIO CAN bus
        - CANivore name or serial number
        - SocketCAN interface (non-FRC Linux only)
        - "*" for any CANivore seen by the program
        - empty string (default) to select the default for the system:

            - "rio" on roboRIO
            - "can0" on Linux
            - "*" on Windows

    :type canbus: str, optional
    """

    def __init__(self, device_id: int, canbus: str = ""):
        super().__init__(device_id, "cancoder", canbus)
        self.configurator = CANcoderConfigurator(self._device_identifier)

        Native.instance().c_ctre_phoenix6_platform_sim_create(DeviceType.PRO_CANcoderType.value, device_id)
        self.__sim_state = None


    @property
    def sim_state(self) -> CANcoderSimState:
        """
        Get the simulation state for this device.

        This function reuses an allocated simulation state
        object, so it is safe to call this function multiple
        times in a robot loop.

        :returns: Simulation state
        :rtype: CANcoderSimState
        """

        if self.__sim_state is None:
            self.__sim_state = CANcoderSimState(self)
        return self.__sim_state


    

    def get_version_major(self) -> StatusSignal[int]:
        """
        App Major Version number.
        
            - Minimum Value: 0
            - Maximum Value: 255
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: VersionMajor Status Signal Object
        :rtype: StatusSignal[int]
        """
        return self._common_lookup(SpnValue.VERSION_MAJOR.value, 0, None, "version_major", False, int)
    
    def get_version_minor(self) -> StatusSignal[int]:
        """
        App Minor Version number.
        
            - Minimum Value: 0
            - Maximum Value: 255
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: VersionMinor Status Signal Object
        :rtype: StatusSignal[int]
        """
        return self._common_lookup(SpnValue.VERSION_MINOR.value, 0, None, "version_minor", False, int)
    
    def get_version_bugfix(self) -> StatusSignal[int]:
        """
        App Bugfix Version number.
        
            - Minimum Value: 0
            - Maximum Value: 255
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: VersionBugfix Status Signal Object
        :rtype: StatusSignal[int]
        """
        return self._common_lookup(SpnValue.VERSION_BUGFIX.value, 0, None, "version_bugfix", False, int)
    
    def get_version_build(self) -> StatusSignal[int]:
        """
        App Build Version number.
        
            - Minimum Value: 0
            - Maximum Value: 255
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: VersionBuild Status Signal Object
        :rtype: StatusSignal[int]
        """
        return self._common_lookup(SpnValue.VERSION_BUILD.value, 0, None, "version_build", False, int)
    
    def get_version(self) -> StatusSignal[int]:
        """
        Full Version.  The format is a four byte value.
        
        Full Version of firmware in device. The format is a four byte value.
        
            - Minimum Value: 0
            - Maximum Value: 4294967295
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Version Status Signal Object
        :rtype: StatusSignal[int]
        """
        return self._common_lookup(SpnValue.VERSION_FULL.value, 0, None, "version", False, int)
    
    def get_fault_field(self) -> StatusSignal[int]:
        """
        Integer representing all faults
        
        This returns the fault flags reported by the device. These are device
        specific and are not used directly in typical applications. Use the
        signal specific GetFault_*() methods instead.  
        
            - Minimum Value: 0
            - Maximum Value: 16777215
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: FaultField Status Signal Object
        :rtype: StatusSignal[int]
        """
        return self._common_lookup(SpnValue.ALL_FAULTS.value, 0, None, "fault_field", True, int)
    
    def get_sticky_fault_field(self) -> StatusSignal[int]:
        """
        Integer representing all sticky faults
        
        This returns the persistent "sticky" fault flags reported by the
        device. These are device specific and are not used directly in typical
        applications. Use the signal specific GetStickyFault_*() methods
        instead.  
        
            - Minimum Value: 0
            - Maximum Value: 16777215
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFaultField Status Signal Object
        :rtype: StatusSignal[int]
        """
        return self._common_lookup(SpnValue.ALL_STICKY_FAULTS.value, 0, None, "sticky_fault_field", True, int)
    
    def get_velocity(self) -> StatusSignal[rotations_per_second]:
        """
        Velocity of the device.
        
            - Minimum Value: -512.0
            - Maximum Value: 511.998046875
            - Default Value: 0
            - Units: rotations per second
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Velocity Status Signal Object
        :rtype: StatusSignal[rotations_per_second]
        """
        return self._common_lookup(SpnValue.CANCODER_VELOCITY.value, 0, None, "velocity", True, rotations_per_second)
    
    def get_position(self) -> StatusSignal[rotation]:
        """
        Position of the device. This is initialized to the absolute position
        on boot.
        
            - Minimum Value: -16384.0
            - Maximum Value: 16383.999755859375
            - Default Value: 0
            - Units: rotations
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Position Status Signal Object
        :rtype: StatusSignal[rotation]
        """
        return self._common_lookup(SpnValue.CANCODER_POSITION.value, 0, None, "position", True, rotation)
    
    def get_absolute_position(self) -> StatusSignal[rotation]:
        """
        Absolute Position of the device. The possible range is documented
        below; however, the exact expected range is determined by the
        AbsoluteSensorRange. This position is only affected by the
        MagnetSensor configs.
        
            - Minimum Value: -0.5
            - Maximum Value: 0.999755859375
            - Default Value: 0
            - Units: rotations
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: AbsolutePosition Status Signal Object
        :rtype: StatusSignal[rotation]
        """
        return self._common_lookup(SpnValue.CANCODER_ABS_POSITION.value, 0, None, "absolute_position", True, rotation)
    
    def get_unfiltered_velocity(self) -> StatusSignal[rotations_per_second]:
        """
        The unfiltered velocity reported by CANcoder.
        
        This is the unfiltered velocity reported by CANcoder. This signal does
        not use the fusing algorithm.
        
            - Minimum Value: -8000.0
            - Maximum Value: 7999.755859375
            - Default Value: 0
            - Units: rotations per second
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: UnfilteredVelocity Status Signal Object
        :rtype: StatusSignal[rotations_per_second]
        """
        return self._common_lookup(SpnValue.CANCODER_RAW_VEL.value, 0, None, "unfiltered_velocity", True, rotations_per_second)
    
    def get_position_since_boot(self) -> StatusSignal[rotation]:
        """
        The relative position reported by the CANcoder since boot.
        
        This is the total displacement reported by CANcoder since power up.
        This signal is relative and is not influenced by the fusing algorithm.
        
            - Minimum Value: -16384.0
            - Maximum Value: 16383.999755859375
            - Default Value: 0
            - Units: rotations
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PositionSinceBoot Status Signal Object
        :rtype: StatusSignal[rotation]
        """
        return self._common_lookup(SpnValue.CANCODER_RAW_POS.value, 0, None, "position_since_boot", True, rotation)
    
    def get_supply_voltage(self) -> StatusSignal[volt]:
        """
        Measured supply voltage to the CANcoder.
        
            - Minimum Value: 4
            - Maximum Value: 16.75
            - Default Value: 4
            - Units: V
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: SupplyVoltage Status Signal Object
        :rtype: StatusSignal[volt]
        """
        return self._common_lookup(SpnValue.CANCODER_SUPPLY_VOLTAGE.value, 0, None, "supply_voltage", True, volt)
    
    def get_magnet_health(self) -> StatusSignal[MagnetHealthValue]:
        """
        Magnet health as measured by CANcoder.
        
        Magnet health as measured by CANcoder. Red indicates too close or too
        far, Orange is adequate but with reduced accuracy, green is ideal.
        Invalid means the accuracy cannot be determined.
        
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: MagnetHealth Status Signal Object
        :rtype: StatusSignal[MagnetHealthValue]
        """
        return self._common_lookup(SpnValue.CANCODER_MAG_HEALTH.value, 0, None, "magnet_health", True, MagnetHealthValue)
    
    def get_is_pro_licensed(self) -> StatusSignal[bool]:
        """
        Whether the device is Phoenix Pro licensed.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: IsProLicensed Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.VERSION_IS_PRO_LICENSED.value, 0, None, "is_pro_licensed", True, bool)
    
    def get_fault_hardware(self) -> StatusSignal[bool]:
        """
        Hardware fault occurred
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_Hardware Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_HARDWARE.value, 0, None, "fault_hardware", True, bool)
    
    def get_sticky_fault_hardware(self) -> StatusSignal[bool]:
        """
        Hardware fault occurred
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_Hardware Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_HARDWARE.value, 0, None, "sticky_fault_hardware", True, bool)
    
    def get_fault_undervoltage(self) -> StatusSignal[bool]:
        """
        Device supply voltage dropped to near brownout levels
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_Undervoltage Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_UNDERVOLTAGE.value, 0, None, "fault_undervoltage", True, bool)
    
    def get_sticky_fault_undervoltage(self) -> StatusSignal[bool]:
        """
        Device supply voltage dropped to near brownout levels
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_Undervoltage Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_UNDERVOLTAGE.value, 0, None, "sticky_fault_undervoltage", True, bool)
    
    def get_fault_boot_during_enable(self) -> StatusSignal[bool]:
        """
        Device boot while detecting the enable signal
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_BootDuringEnable Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_BOOT_DURING_ENABLE.value, 0, None, "fault_boot_during_enable", True, bool)
    
    def get_sticky_fault_boot_during_enable(self) -> StatusSignal[bool]:
        """
        Device boot while detecting the enable signal
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_BootDuringEnable Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_BOOT_DURING_ENABLE.value, 0, None, "sticky_fault_boot_during_enable", True, bool)
    
    def get_fault_unlicensed_feature_in_use(self) -> StatusSignal[bool]:
        """
        An unlicensed feature is in use, device may not behave as expected.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_UnlicensedFeatureInUse Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_UNLICENSED_FEATURE_IN_USE.value, 0, None, "fault_unlicensed_feature_in_use", True, bool)
    
    def get_sticky_fault_unlicensed_feature_in_use(self) -> StatusSignal[bool]:
        """
        An unlicensed feature is in use, device may not behave as expected.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_UnlicensedFeatureInUse Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_UNLICENSED_FEATURE_IN_USE.value, 0, None, "sticky_fault_unlicensed_feature_in_use", True, bool)
    
    def get_fault_bad_magnet(self) -> StatusSignal[bool]:
        """
        The magnet distance is not correct or magnet is missing
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_BadMagnet Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_CANCODER_BAD_MAGNET.value, 0, None, "fault_bad_magnet", True, bool)
    
    def get_sticky_fault_bad_magnet(self) -> StatusSignal[bool]:
        """
        The magnet distance is not correct or magnet is missing
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_BadMagnet Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_CANCODER_BAD_MAGNET.value, 0, None, "sticky_fault_bad_magnet", True, bool)
    

    def set_control(self, request: SupportsSendRequest) -> StatusCode:
        """
        Control motor with generic control request object.

        If control request is not supported by device, this request
        will fail with StatusCode NotSupported

        :param request: Control object to request of the device
        :type request: SupportsSendRequest
        :return: StatusCode of the request
        :rtype: StatusCode
        """
        if isinstance(request, ()):
            return self._set_control_private(request)
        return StatusCode.NOT_SUPPORTED

    
    def set_position(self, new_value: rotation, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Sets the current position of the device.
        
        :param new_value: Value to set to. Units are in rotations.
        :type new_value: rotation
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.set_position(new_value, timeout_seconds)
    
    def clear_sticky_faults(self, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Clear the sticky faults in the device.
        
        This typically has no impact on the device functionality.  Instead, it
        just clears telemetry faults that are accessible via API and Tuner
        Self-Test.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_faults(timeout_seconds)
    
    def clear_sticky_fault_hardware(self, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Clear sticky fault: Hardware fault occurred
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_hardware(timeout_seconds)
    
    def clear_sticky_fault_undervoltage(self, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Clear sticky fault: Device supply voltage dropped to near brownout
        levels
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_undervoltage(timeout_seconds)
    
    def clear_sticky_fault_boot_during_enable(self, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Clear sticky fault: Device boot while detecting the enable signal
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_boot_during_enable(timeout_seconds)
    
    def clear_sticky_fault_bad_magnet(self, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Clear sticky fault: The magnet distance is not correct or magnet is
        missing
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_bad_magnet(timeout_seconds)

