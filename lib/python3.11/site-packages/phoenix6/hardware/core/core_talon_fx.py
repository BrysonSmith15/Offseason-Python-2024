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
from phoenix6.controls.duty_cycle_out import DutyCycleOut
from phoenix6.controls.torque_current_foc import TorqueCurrentFOC
from phoenix6.controls.voltage_out import VoltageOut
from phoenix6.controls.position_duty_cycle import PositionDutyCycle
from phoenix6.controls.position_voltage import PositionVoltage
from phoenix6.controls.position_torque_current_foc import PositionTorqueCurrentFOC
from phoenix6.controls.velocity_duty_cycle import VelocityDutyCycle
from phoenix6.controls.velocity_voltage import VelocityVoltage
from phoenix6.controls.velocity_torque_current_foc import VelocityTorqueCurrentFOC
from phoenix6.controls.motion_magic_duty_cycle import MotionMagicDutyCycle
from phoenix6.controls.motion_magic_voltage import MotionMagicVoltage
from phoenix6.controls.motion_magic_torque_current_foc import MotionMagicTorqueCurrentFOC
from phoenix6.controls.differential_duty_cycle import DifferentialDutyCycle
from phoenix6.controls.differential_voltage import DifferentialVoltage
from phoenix6.controls.differential_position_duty_cycle import DifferentialPositionDutyCycle
from phoenix6.controls.differential_position_voltage import DifferentialPositionVoltage
from phoenix6.controls.differential_velocity_duty_cycle import DifferentialVelocityDutyCycle
from phoenix6.controls.differential_velocity_voltage import DifferentialVelocityVoltage
from phoenix6.controls.differential_motion_magic_duty_cycle import DifferentialMotionMagicDutyCycle
from phoenix6.controls.differential_motion_magic_voltage import DifferentialMotionMagicVoltage
from phoenix6.controls.follower import Follower
from phoenix6.controls.strict_follower import StrictFollower
from phoenix6.controls.differential_follower import DifferentialFollower
from phoenix6.controls.differential_strict_follower import DifferentialStrictFollower
from phoenix6.controls.neutral_out import NeutralOut
from phoenix6.controls.coast_out import CoastOut
from phoenix6.controls.static_brake import StaticBrake
from phoenix6.controls.music_tone import MusicTone
from phoenix6.controls.motion_magic_velocity_duty_cycle import MotionMagicVelocityDutyCycle
from phoenix6.controls.motion_magic_velocity_torque_current_foc import MotionMagicVelocityTorqueCurrentFOC
from phoenix6.controls.motion_magic_velocity_voltage import MotionMagicVelocityVoltage
from phoenix6.controls.motion_magic_expo_duty_cycle import MotionMagicExpoDutyCycle
from phoenix6.controls.motion_magic_expo_voltage import MotionMagicExpoVoltage
from phoenix6.controls.motion_magic_expo_torque_current_foc import MotionMagicExpoTorqueCurrentFOC
from phoenix6.controls.dynamic_motion_magic_duty_cycle import DynamicMotionMagicDutyCycle
from phoenix6.controls.dynamic_motion_magic_voltage import DynamicMotionMagicVoltage
from phoenix6.controls.dynamic_motion_magic_torque_current_foc import DynamicMotionMagicTorqueCurrentFOC
from phoenix6.configs.talon_fx_configs import TalonFXConfigurator
from phoenix6.signals.spn_enums import ForwardLimitValue, ReverseLimitValue, AppliedRotorPolarityValue, ControlModeValue, MotionMagicIsRunningValue, DeviceEnableValue, DifferentialControlModeValue, BridgeOutputValue, MotorTypeValue, MotorOutputStatusValue
from phoenix6.sim.talon_fx_sim_state import TalonFXSimState

class CoreTalonFX(ParentDevice):
    """
    Constructs a new Talon FX motor controller object.

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
        super().__init__(device_id, "talon fx", canbus)
        self.configurator = TalonFXConfigurator(self._device_identifier)

        Native.instance().c_ctre_phoenix6_platform_sim_create(DeviceType.PRO_TalonFXType.value, device_id)
        self.__sim_state = None


    @property
    def sim_state(self) -> TalonFXSimState:
        """
        Get the simulation state for this device.

        This function reuses an allocated simulation state
        object, so it is safe to call this function multiple
        times in a robot loop.

        :returns: Simulation state
        :rtype: TalonFXSimState
        """

        if self.__sim_state is None:
            self.__sim_state = TalonFXSimState(self)
        return self.__sim_state


    def _get_pid_duty_cycle_proportional_output(self) -> StatusSignal[float]:
        """
        Proportional output of PID controller when PID'ing under a DutyCycle
        Request
        
            - Minimum Value: -128.0
            - Maximum Value: 127.9990234375
            - Default Value: 0
            - Units: fractional
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PIDDutyCycle_ProportionalOutput Status Signal Object
        :rtype: StatusSignal[float]
        """
        return self._common_lookup(SpnValue.PRO_PIDOUTPUT_PROPORTIONAL_OUTPUT_DC.value, 0, None, "pid_duty_cycle_proportional_output", True, float)
    
    def _get_pid_motor_voltage_proportional_output(self) -> StatusSignal[volt]:
        """
        Proportional output of PID controller when PID'ing under a Voltage
        Request
        
            - Minimum Value: -1310.72
            - Maximum Value: 1310.71
            - Default Value: 0
            - Units: V
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PIDMotorVoltage_ProportionalOutput Status Signal Object
        :rtype: StatusSignal[volt]
        """
        return self._common_lookup(SpnValue.PRO_PIDOUTPUT_PROPORTIONAL_OUTPUT_V.value, 0, None, "pid_motor_voltage_proportional_output", True, volt)
    
    def _get_pid_torque_current_proportional_output(self) -> StatusSignal[ampere]:
        """
        Proportional output of PID controller when PID'ing under a
        TorqueCurrent Request
        
            - Minimum Value: -13107.2
            - Maximum Value: 13107.1
            - Default Value: 0
            - Units: A
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PIDTorqueCurrent_ProportionalOutput Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        return self._common_lookup(SpnValue.PRO_PIDOUTPUT_PROPORTIONAL_OUTPUT_A.value, 0, None, "pid_torque_current_proportional_output", True, ampere)
    
    def _get_pid_duty_cycle_integrated_accum(self) -> StatusSignal[float]:
        """
        Integrated Accumulator of PID controller when PID'ing under a
        DutyCycle Request
        
            - Minimum Value: -128.0
            - Maximum Value: 127.9990234375
            - Default Value: 0
            - Units: fractional
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PIDDutyCycle_IntegratedAccum Status Signal Object
        :rtype: StatusSignal[float]
        """
        return self._common_lookup(SpnValue.PRO_PIDSTATE_ENABLES_INTEGRATED_ACCUM_DC.value, 0, None, "pid_duty_cycle_integrated_accum", True, float)
    
    def _get_pid_motor_voltage_integrated_accum(self) -> StatusSignal[volt]:
        """
        Integrated Accumulator of PID controller when PID'ing under a Voltage
        Request
        
            - Minimum Value: -1310.72
            - Maximum Value: 1310.71
            - Default Value: 0
            - Units: V
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PIDMotorVoltage_IntegratedAccum Status Signal Object
        :rtype: StatusSignal[volt]
        """
        return self._common_lookup(SpnValue.PRO_PIDSTATE_ENABLES_INTEGRATED_ACCUM_V.value, 0, None, "pid_motor_voltage_integrated_accum", True, volt)
    
    def _get_pid_torque_current_integrated_accum(self) -> StatusSignal[ampere]:
        """
        Integrated Accumulator of PID controller when PID'ing under a
        TorqueCurrent Request
        
            - Minimum Value: -13107.2
            - Maximum Value: 13107.1
            - Default Value: 0
            - Units: A
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PIDTorqueCurrent_IntegratedAccum Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        return self._common_lookup(SpnValue.PRO_PIDSTATE_ENABLES_INTEGRATED_ACCUM_A.value, 0, None, "pid_torque_current_integrated_accum", True, ampere)
    
    def _get_pid_duty_cycle_feed_forward(self) -> StatusSignal[float]:
        """
        Feedforward passed to PID controller
        
            - Minimum Value: -2.0
            - Maximum Value: 1.9990234375
            - Default Value: 0
            - Units: fractional
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PIDDutyCycle_FeedForward Status Signal Object
        :rtype: StatusSignal[float]
        """
        return self._common_lookup(SpnValue.PRO_PIDSTATE_ENABLES_FEED_FORWARD_DC.value, 0, None, "pid_duty_cycle_feed_forward", True, float)
    
    def _get_pid_motor_voltage_feed_forward(self) -> StatusSignal[volt]:
        """
        Feedforward passed to PID controller
        
            - Minimum Value: -20.48
            - Maximum Value: 20.47
            - Default Value: 0
            - Units: V
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PIDMotorVoltage_FeedForward Status Signal Object
        :rtype: StatusSignal[volt]
        """
        return self._common_lookup(SpnValue.PRO_PIDSTATE_ENABLES_FEED_FORWARD_V.value, 0, None, "pid_motor_voltage_feed_forward", True, volt)
    
    def _get_pid_torque_current_feed_forward(self) -> StatusSignal[ampere]:
        """
        Feedforward passed to PID controller
        
            - Minimum Value: -409.6
            - Maximum Value: 409.40000000000003
            - Default Value: 0
            - Units: A
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PIDTorqueCurrent_FeedForward Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        return self._common_lookup(SpnValue.PRO_PIDSTATE_ENABLES_FEED_FORWARD_A.value, 0, None, "pid_torque_current_feed_forward", True, ampere)
    
    def _get_pid_duty_cycle_derivative_output(self) -> StatusSignal[float]:
        """
        Derivative Output of PID controller when PID'ing under a DutyCycle
        Request
        
            - Minimum Value: -128.0
            - Maximum Value: 127.9990234375
            - Default Value: 0
            - Units: fractional
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PIDDutyCycle_DerivativeOutput Status Signal Object
        :rtype: StatusSignal[float]
        """
        return self._common_lookup(SpnValue.PRO_PIDOUTPUT_DERIVATIVE_OUTPUT_DC.value, 0, None, "pid_duty_cycle_derivative_output", True, float)
    
    def _get_pid_motor_voltage_derivative_output(self) -> StatusSignal[volt]:
        """
        Derivative Output of PID controller when PID'ing under a Voltage
        Request
        
            - Minimum Value: -1310.72
            - Maximum Value: 1310.71
            - Default Value: 0
            - Units: V
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PIDMotorVoltage_DerivativeOutput Status Signal Object
        :rtype: StatusSignal[volt]
        """
        return self._common_lookup(SpnValue.PRO_PIDOUTPUT_DERIVATIVE_OUTPUT_V.value, 0, None, "pid_motor_voltage_derivative_output", True, volt)
    
    def _get_pid_torque_current_derivative_output(self) -> StatusSignal[ampere]:
        """
        Derivative Output of PID controller when PID'ing under a TorqueCurrent
        Request
        
            - Minimum Value: -13107.2
            - Maximum Value: 13107.1
            - Default Value: 0
            - Units: A
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PIDTorqueCurrent_DerivativeOutput Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        return self._common_lookup(SpnValue.PRO_PIDOUTPUT_DERIVATIVE_OUTPUT_A.value, 0, None, "pid_torque_current_derivative_output", True, ampere)
    
    def _get_pid_duty_cycle_output(self) -> StatusSignal[float]:
        """
        Output of PID controller when PID'ing under a DutyCycle Request
        
            - Minimum Value: -128.0
            - Maximum Value: 127.9990234375
            - Default Value: 0
            - Units: fractional
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PIDDutyCycle_Output Status Signal Object
        :rtype: StatusSignal[float]
        """
        return self._common_lookup(SpnValue.PRO_PIDOUTPUT_OUTPUT_DC.value, 0, None, "pid_duty_cycle_output", True, float)
    
    def _get_pid_motor_voltage_output(self) -> StatusSignal[volt]:
        """
        Output of PID controller when PID'ing under a Voltage Request
        
            - Minimum Value: -1310.72
            - Maximum Value: 1310.71
            - Default Value: 0
            - Units: V
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PIDMotorVoltage_Output Status Signal Object
        :rtype: StatusSignal[volt]
        """
        return self._common_lookup(SpnValue.PRO_PIDOUTPUT_OUTPUT_V.value, 0, None, "pid_motor_voltage_output", True, volt)
    
    def _get_pid_torque_current_output(self) -> StatusSignal[ampere]:
        """
        Output of PID controller when PID'ing under a TorqueCurrent Request
        
            - Minimum Value: -13107.2
            - Maximum Value: 13107.1
            - Default Value: 0
            - Units: A
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PIDTorqueCurrent_Output Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        return self._common_lookup(SpnValue.PRO_PIDOUTPUT_OUTPUT_A.value, 0, None, "pid_torque_current_output", True, ampere)
    
    def _get_pid_position_reference(self) -> StatusSignal[rotation]:
        """
        Input position of PID controller when PID'ing to a position
        
            - Minimum Value: -10000
            - Maximum Value: 10000
            - Default Value: 0
            - Units: rotations
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PIDPosition_Reference Status Signal Object
        :rtype: StatusSignal[rotation]
        """
        return self._common_lookup(SpnValue.PRO_PIDREF_PIDERR_PIDREF_POSITION.value, 0, None, "pid_position_reference", True, rotation)
    
    def _get_pid_velocity_reference(self) -> StatusSignal[rotations_per_second]:
        """
        Input velocity of PID controller when PID'ing to a velocity
        
            - Minimum Value: -10000
            - Maximum Value: 10000
            - Default Value: 0
            - Units: rotations per second
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PIDVelocity_Reference Status Signal Object
        :rtype: StatusSignal[rotations_per_second]
        """
        return self._common_lookup(SpnValue.PRO_PIDREF_PIDERR_PIDREF_VELOCITY.value, 0, None, "pid_velocity_reference", True, rotations_per_second)
    
    def _get_pid_position_reference_slope(self) -> StatusSignal[rotations_per_second]:
        """
        Change in input (velocity) of PID controller when PID'ing to a
        position
        
            - Minimum Value: -512.0
            - Maximum Value: 511.984375
            - Default Value: 0
            - Units: rotations per second
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PIDPosition_ReferenceSlope Status Signal Object
        :rtype: StatusSignal[rotations_per_second]
        """
        return self._common_lookup(SpnValue.PRO_PIDREF_SLOPE_ECUTIME_REFERENCE_SLOPE_POSITION.value, 0, None, "pid_position_reference_slope", True, rotations_per_second)
    
    def _get_pid_velocity_reference_slope(self) -> StatusSignal[rotations_per_second_squared]:
        """
        Change in input (acceleration) of PID controller when PID'ing to a
        velocity
        
            - Minimum Value: -512.0
            - Maximum Value: 511.984375
            - Default Value: 0
            - Units: rotations per second²
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PIDVelocity_ReferenceSlope Status Signal Object
        :rtype: StatusSignal[rotations_per_second_squared]
        """
        return self._common_lookup(SpnValue.PRO_PIDREF_SLOPE_ECUTIME_REFERENCE_SLOPE_VELOCITY.value, 0, None, "pid_velocity_reference_slope", True, rotations_per_second_squared)
    
    def _get_pid_position_closed_loop_error(self) -> StatusSignal[rotation]:
        """
        The difference between target position and current position
        
            - Minimum Value: -10000
            - Maximum Value: 10000
            - Default Value: 0
            - Units: rotations
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PIDPosition_ClosedLoopError Status Signal Object
        :rtype: StatusSignal[rotation]
        """
        return self._common_lookup(SpnValue.PRO_PIDREF_PIDERR_PIDERR_POSITION.value, 0, None, "pid_position_closed_loop_error", True, rotation)
    
    def _get_pid_velocity_closed_loop_error(self) -> StatusSignal[rotations_per_second]:
        """
        The difference between target velocity and current velocity
        
            - Minimum Value: -10000
            - Maximum Value: 10000
            - Default Value: 0
            - Units: rotations per second
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: PIDVelocity_ClosedLoopError Status Signal Object
        :rtype: StatusSignal[rotations_per_second]
        """
        return self._common_lookup(SpnValue.PRO_PIDREF_PIDERR_PIDERR_VELOCITY.value, 0, None, "pid_velocity_closed_loop_error", True, rotations_per_second)
    
    def _get_differential_duty_cycle(self) -> StatusSignal[float]:
        """
        The calculated motor duty cycle for differential followers.
        
            - Minimum Value: -32.0
            - Maximum Value: 31.9990234375
            - Default Value: 0
            - Units: fractional
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialDutyCycle Status Signal Object
        :rtype: StatusSignal[float]
        """
        return self._common_lookup(SpnValue.PRO_MOTOR_OUTPUT_PIDSTATE_DIFF_DUTY_CYCLE.value, 0, None, "differential_duty_cycle", True, float)
    
    def _get_differential_torque_current(self) -> StatusSignal[ampere]:
        """
        The calculated motor torque current for differential followers.
        
            - Minimum Value: -327.68
            - Maximum Value: 327.67
            - Default Value: 0
            - Units: A
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialTorqueCurrent Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        return self._common_lookup(SpnValue.PRO_MOTOR_OUTPUT_PIDSTATE_DIFF_TORQUE_CURRENT.value, 0, None, "differential_torque_current", True, ampere)
    
    def _get_differential_pid_duty_cycle_proportional_output(self) -> StatusSignal[float]:
        """
        Proportional output of differential PID controller when PID'ing under
        a DutyCycle Request
        
            - Minimum Value: -128.0
            - Maximum Value: 127.9990234375
            - Default Value: 0
            - Units: fractional
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialPIDDutyCycle_ProportionalOutput Status Signal Object
        :rtype: StatusSignal[float]
        """
        return self._common_lookup(SpnValue.PRO_DIFF_PIDOUTPUT_PROPORTIONAL_OUTPUT_DC.value, 0, None, "differential_pid_duty_cycle_proportional_output", True, float)
    
    def _get_differential_pid_motor_voltage_proportional_output(self) -> StatusSignal[volt]:
        """
        Proportional output of differential PID controller when PID'ing under
        a Voltage Request
        
            - Minimum Value: -1310.72
            - Maximum Value: 1310.71
            - Default Value: 0
            - Units: V
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialPIDMotorVoltage_ProportionalOutput Status Signal Object
        :rtype: StatusSignal[volt]
        """
        return self._common_lookup(SpnValue.PRO_DIFF_PIDOUTPUT_PROPORTIONAL_OUTPUT_V.value, 0, None, "differential_pid_motor_voltage_proportional_output", True, volt)
    
    def _get_differential_pid_torque_current_proportional_output(self) -> StatusSignal[ampere]:
        """
        Proportional output of differential PID controller when PID'ing under
        a TorqueCurrent Request
        
            - Minimum Value: -13107.2
            - Maximum Value: 13107.1
            - Default Value: 0
            - Units: A
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialPIDTorqueCurrent_ProportionalOutput Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        return self._common_lookup(SpnValue.PRO_DIFF_PIDOUTPUT_PROPORTIONAL_OUTPUT_A.value, 0, None, "differential_pid_torque_current_proportional_output", True, ampere)
    
    def _get_differential_pid_duty_cycle_integrated_accum(self) -> StatusSignal[float]:
        """
        Integrated Accumulator of differential PID controller when PID'ing
        under a DutyCycle Request
        
            - Minimum Value: -128.0
            - Maximum Value: 127.9990234375
            - Default Value: 0
            - Units: fractional
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialPIDDutyCycle_IntegratedAccum Status Signal Object
        :rtype: StatusSignal[float]
        """
        return self._common_lookup(SpnValue.PRO_MOTOR_OUTPUT_PIDSTATE_DIFF_INTEGRATED_ACCUM_DC.value, 0, None, "differential_pid_duty_cycle_integrated_accum", True, float)
    
    def _get_differential_pid_motor_voltage_integrated_accum(self) -> StatusSignal[volt]:
        """
        Integrated Accumulator of differential PID controller when PID'ing
        under a Voltage Request
        
            - Minimum Value: -1310.72
            - Maximum Value: 1310.71
            - Default Value: 0
            - Units: V
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialPIDMotorVoltage_IntegratedAccum Status Signal Object
        :rtype: StatusSignal[volt]
        """
        return self._common_lookup(SpnValue.PRO_MOTOR_OUTPUT_PIDSTATE_DIFF_INTEGRATED_ACCUM_V.value, 0, None, "differential_pid_motor_voltage_integrated_accum", True, volt)
    
    def _get_differential_pid_torque_current_integrated_accum(self) -> StatusSignal[ampere]:
        """
        Integrated Accumulator of differential PID controller when PID'ing
        under a TorqueCurrent Request
        
            - Minimum Value: -13107.2
            - Maximum Value: 13107.1
            - Default Value: 0
            - Units: A
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialPIDTorqueCurrent_IntegratedAccum Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        return self._common_lookup(SpnValue.PRO_MOTOR_OUTPUT_PIDSTATE_DIFF_INTEGRATED_ACCUM_A.value, 0, None, "differential_pid_torque_current_integrated_accum", True, ampere)
    
    def _get_differential_pid_duty_cycle_feed_forward(self) -> StatusSignal[float]:
        """
        Feedforward passed to differential PID controller
        
            - Minimum Value: -2.0
            - Maximum Value: 1.9990234375
            - Default Value: 0
            - Units: fractional
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialPIDDutyCycle_FeedForward Status Signal Object
        :rtype: StatusSignal[float]
        """
        return self._common_lookup(SpnValue.PRO_MOTOR_OUTPUT_PIDSTATE_DIFF_FEED_FORWARD_DC.value, 0, None, "differential_pid_duty_cycle_feed_forward", True, float)
    
    def _get_differential_pid_motor_voltage_feed_forward(self) -> StatusSignal[volt]:
        """
        Feedforward passed to differential PID controller
        
            - Minimum Value: -20.48
            - Maximum Value: 20.47
            - Default Value: 0
            - Units: V
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialPIDMotorVoltage_FeedForward Status Signal Object
        :rtype: StatusSignal[volt]
        """
        return self._common_lookup(SpnValue.PRO_MOTOR_OUTPUT_PIDSTATE_DIFF_FEED_FORWARD_V.value, 0, None, "differential_pid_motor_voltage_feed_forward", True, volt)
    
    def _get_differential_pid_torque_current_feed_forward(self) -> StatusSignal[ampere]:
        """
        Feedforward passed to differential PID controller
        
            - Minimum Value: -409.6
            - Maximum Value: 409.40000000000003
            - Default Value: 0
            - Units: A
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialPIDTorqueCurrent_FeedForward Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        return self._common_lookup(SpnValue.PRO_MOTOR_OUTPUT_PIDSTATE_DIFF_FEED_FORWARD_A.value, 0, None, "differential_pid_torque_current_feed_forward", True, ampere)
    
    def _get_differential_pid_duty_cycle_derivative_output(self) -> StatusSignal[float]:
        """
        Derivative Output of differential PID controller when PID'ing under a
        DutyCycle Request
        
            - Minimum Value: -128.0
            - Maximum Value: 127.9990234375
            - Default Value: 0
            - Units: fractional
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialPIDDutyCycle_DerivativeOutput Status Signal Object
        :rtype: StatusSignal[float]
        """
        return self._common_lookup(SpnValue.PRO_DIFF_PIDOUTPUT_DERIVATIVE_OUTPUT_DC.value, 0, None, "differential_pid_duty_cycle_derivative_output", True, float)
    
    def _get_diff_pid_motor_voltage_derivative_output(self) -> StatusSignal[volt]:
        """
        Derivative Output of differential PID controller when PID'ing under a
        Voltage Request
        
            - Minimum Value: -1310.72
            - Maximum Value: 1310.71
            - Default Value: 0
            - Units: V
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DiffPIDMotorVoltage_DerivativeOutput Status Signal Object
        :rtype: StatusSignal[volt]
        """
        return self._common_lookup(SpnValue.PRO_DIFF_PIDOUTPUT_DERIVATIVE_OUTPUT_V.value, 0, None, "diff_pid_motor_voltage_derivative_output", True, volt)
    
    def _get_differential_pid_torque_current_derivative_output(self) -> StatusSignal[ampere]:
        """
        Derivative Output of differential PID controller when PID'ing under a
        TorqueCurrent Request
        
            - Minimum Value: -13107.2
            - Maximum Value: 13107.1
            - Default Value: 0
            - Units: A
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialPIDTorqueCurrent_DerivativeOutput Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        return self._common_lookup(SpnValue.PRO_DIFF_PIDOUTPUT_DERIVATIVE_OUTPUT_A.value, 0, None, "differential_pid_torque_current_derivative_output", True, ampere)
    
    def _get_differential_pid_duty_cycle_output(self) -> StatusSignal[float]:
        """
        Output of differential PID controller when PID'ing under a DutyCycle
        Request
        
            - Minimum Value: -128.0
            - Maximum Value: 127.9990234375
            - Default Value: 0
            - Units: fractional
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialPIDDutyCycle_Output Status Signal Object
        :rtype: StatusSignal[float]
        """
        return self._common_lookup(SpnValue.PRO_DIFF_PIDOUTPUT_OUTPUT_DC.value, 0, None, "differential_pid_duty_cycle_output", True, float)
    
    def _get_differential_pid_motor_voltage_output(self) -> StatusSignal[volt]:
        """
        Output of differential PID controller when PID'ing under a Voltage
        Request
        
            - Minimum Value: -1310.72
            - Maximum Value: 1310.71
            - Default Value: 0
            - Units: V
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialPIDMotorVoltage_Output Status Signal Object
        :rtype: StatusSignal[volt]
        """
        return self._common_lookup(SpnValue.PRO_DIFF_PIDOUTPUT_OUTPUT_V.value, 0, None, "differential_pid_motor_voltage_output", True, volt)
    
    def _get_differential_pid_torque_current_output(self) -> StatusSignal[ampere]:
        """
        Output of differential PID controller when PID'ing under a
        TorqueCurrent Request
        
            - Minimum Value: -13107.2
            - Maximum Value: 13107.1
            - Default Value: 0
            - Units: A
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialPIDTorqueCurrent_Output Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        return self._common_lookup(SpnValue.PRO_DIFF_PIDOUTPUT_OUTPUT_A.value, 0, None, "differential_pid_torque_current_output", True, ampere)
    
    def _get_differential_pid_position_reference(self) -> StatusSignal[rotation]:
        """
        Input position of differential PID controller when PID'ing to a
        differential position
        
            - Minimum Value: -10000
            - Maximum Value: 10000
            - Default Value: 0
            - Units: rotations
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialPIDPosition_Reference Status Signal Object
        :rtype: StatusSignal[rotation]
        """
        return self._common_lookup(SpnValue.PRO_DIFF_PIDREF_PIDERR_PIDREF_POSITION.value, 0, None, "differential_pid_position_reference", True, rotation)
    
    def _get_differential_pid_velocity_reference(self) -> StatusSignal[rotations_per_second]:
        """
        Input velocity of differential PID controller when PID'ing to a
        differential velocity
        
            - Minimum Value: -10000
            - Maximum Value: 10000
            - Default Value: 0
            - Units: rotations per second
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialPIDVelocity_Reference Status Signal Object
        :rtype: StatusSignal[rotations_per_second]
        """
        return self._common_lookup(SpnValue.PRO_DIFF_PIDREF_PIDERR_PIDREF_VELOCITY.value, 0, None, "differential_pid_velocity_reference", True, rotations_per_second)
    
    def _get_differential_pid_position_reference_slope(self) -> StatusSignal[rotations_per_second]:
        """
        Change in input (velocity) of differential PID controller when PID'ing
        to a differential position
        
            - Minimum Value: -512.0
            - Maximum Value: 511.984375
            - Default Value: 0
            - Units: rotations per second
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialPIDPosition_ReferenceSlope Status Signal Object
        :rtype: StatusSignal[rotations_per_second]
        """
        return self._common_lookup(SpnValue.PRO_DIFF_PIDREF_SLOPE_ECUTIME_REFERENCE_SLOPE_POSITION.value, 0, None, "differential_pid_position_reference_slope", True, rotations_per_second)
    
    def _get_differential_pid_velocity_reference_slope(self) -> StatusSignal[rotations_per_second_squared]:
        """
        Change in input (acceleration) of differential PID controller when
        PID'ing to a differential velocity
        
            - Minimum Value: -512.0
            - Maximum Value: 511.984375
            - Default Value: 0
            - Units: rotations per second²
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialPIDVelocity_ReferenceSlope Status Signal Object
        :rtype: StatusSignal[rotations_per_second_squared]
        """
        return self._common_lookup(SpnValue.PRO_DIFF_PIDREF_SLOPE_ECUTIME_REFERENCE_SLOPE_VELOCITY.value, 0, None, "differential_pid_velocity_reference_slope", True, rotations_per_second_squared)
    
    def _get_differential_pid_position_closed_loop_error(self) -> StatusSignal[rotation]:
        """
        The difference between target differential position and current
        differential position
        
            - Minimum Value: -10000
            - Maximum Value: 10000
            - Default Value: 0
            - Units: rotations
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialPIDPosition_ClosedLoopError Status Signal Object
        :rtype: StatusSignal[rotation]
        """
        return self._common_lookup(SpnValue.PRO_DIFF_PIDREF_PIDERR_PIDERR_POSITION.value, 0, None, "differential_pid_position_closed_loop_error", True, rotation)
    
    def _get_differential_pid_velocity_closed_loop_error(self) -> StatusSignal[rotations_per_second]:
        """
        The difference between target differential velocity and current
        differential velocity
        
            - Minimum Value: -10000
            - Maximum Value: 10000
            - Default Value: 0
            - Units: rotations per second
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialPIDVelocity_ClosedLoopError Status Signal Object
        :rtype: StatusSignal[rotations_per_second]
        """
        return self._common_lookup(SpnValue.PRO_DIFF_PIDREF_PIDERR_PIDERR_VELOCITY.value, 0, None, "differential_pid_velocity_closed_loop_error", True, rotations_per_second)
    

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
    
    def get_motor_voltage(self) -> StatusSignal[volt]:
        """
        The applied (output) motor voltage.
        
            - Minimum Value: -40.96
            - Maximum Value: 40.95
            - Default Value: 0
            - Units: V
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: MotorVoltage Status Signal Object
        :rtype: StatusSignal[volt]
        """
        return self._common_lookup(SpnValue.PRO_MOTOR_OUTPUT_MOTOR_VOLTAGE.value, 0, None, "motor_voltage", True, volt)
    
    def get_forward_limit(self) -> StatusSignal[ForwardLimitValue]:
        """
        Forward Limit Pin.
        
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: ForwardLimit Status Signal Object
        :rtype: StatusSignal[ForwardLimitValue]
        """
        return self._common_lookup(SpnValue.FORWARD_LIMIT.value, 0, None, "forward_limit", True, ForwardLimitValue)
    
    def get_reverse_limit(self) -> StatusSignal[ReverseLimitValue]:
        """
        Reverse Limit Pin.
        
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: ReverseLimit Status Signal Object
        :rtype: StatusSignal[ReverseLimitValue]
        """
        return self._common_lookup(SpnValue.REVERSE_LIMIT.value, 0, None, "reverse_limit", True, ReverseLimitValue)
    
    def get_applied_rotor_polarity(self) -> StatusSignal[AppliedRotorPolarityValue]:
        """
        The applied rotor polarity.  This typically is determined by the
        Inverted config, but can be overridden if using Follower features.
        
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: AppliedRotorPolarity Status Signal Object
        :rtype: StatusSignal[AppliedRotorPolarityValue]
        """
        return self._common_lookup(SpnValue.PRO_MOTOR_OUTPUT_ROTOR_POLARITY.value, 0, None, "applied_rotor_polarity", True, AppliedRotorPolarityValue)
    
    def get_duty_cycle(self) -> StatusSignal[float]:
        """
        The applied motor duty cycle.
        
            - Minimum Value: -2.0
            - Maximum Value: 1.9990234375
            - Default Value: 0
            - Units: fractional
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DutyCycle Status Signal Object
        :rtype: StatusSignal[float]
        """
        return self._common_lookup(SpnValue.PRO_MOTOR_OUTPUT_DUTY_CYCLE.value, 0, None, "duty_cycle", True, float)
    
    def get_torque_current(self) -> StatusSignal[ampere]:
        """
        Current corresponding to the torque output by the motor. Similar to
        StatorCurrent. Users will likely prefer this current to calculate the
        applied torque to the rotor.
        
        Stator current where positive current means torque is applied in the
        forward direction as determined by the Inverted setting
        
            - Minimum Value: -327.68
            - Maximum Value: 327.67
            - Default Value: 0
            - Units: A
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: TorqueCurrent Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        return self._common_lookup(SpnValue.PRO_MOTOR_OUTPUT_TORQUE_CURRENT.value, 0, None, "torque_current", True, ampere)
    
    def get_stator_current(self) -> StatusSignal[ampere]:
        """
        Current corresponding to the stator windings. Similar to
        TorqueCurrent. Users will likely prefer TorqueCurrent over
        StatorCurrent.
        
        Stator current where Positive current indicates motoring regardless of
        direction. Negative current indicates regenerative braking regardless
        of direction.
        
            - Minimum Value: -327.68
            - Maximum Value: 327.66
            - Default Value: 0
            - Units: A
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StatorCurrent Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        return self._common_lookup(SpnValue.PRO_SUPPLY_AND_TEMP_STATOR_CURRENT.value, 0, None, "stator_current", True, ampere)
    
    def get_supply_current(self) -> StatusSignal[ampere]:
        """
        Measured supply side current
        
            - Minimum Value: -327.68
            - Maximum Value: 327.66
            - Default Value: 0
            - Units: A
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: SupplyCurrent Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        return self._common_lookup(SpnValue.PRO_SUPPLY_AND_TEMP_SUPPLY_CURRENT.value, 0, None, "supply_current", True, ampere)
    
    def get_supply_voltage(self) -> StatusSignal[volt]:
        """
        Measured supply voltage to the TalonFX.
        
            - Minimum Value: 4
            - Maximum Value: 29.575
            - Default Value: 4
            - Units: V
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: SupplyVoltage Status Signal Object
        :rtype: StatusSignal[volt]
        """
        return self._common_lookup(SpnValue.PRO_SUPPLY_AND_TEMP_SUPPLY_VOLTAGE.value, 0, None, "supply_voltage", True, volt)
    
    def get_device_temp(self) -> StatusSignal[celsius]:
        """
        Temperature of device
        
        This is the temperature that the device measures itself to be at.
        Similar to Processor Temperature.
        
            - Minimum Value: 0.0
            - Maximum Value: 255.0
            - Default Value: 0
            - Units: ℃
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DeviceTemp Status Signal Object
        :rtype: StatusSignal[celsius]
        """
        return self._common_lookup(SpnValue.PRO_SUPPLY_AND_TEMP_DEVICE_TEMP.value, 0, None, "device_temp", True, celsius)
    
    def get_processor_temp(self) -> StatusSignal[celsius]:
        """
        Temperature of the processor
        
        This is the temperature that the processor measures itself to be at.
        Similar to Device Temperature.
        
            - Minimum Value: 0.0
            - Maximum Value: 255.0
            - Default Value: 0
            - Units: ℃
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: ProcessorTemp Status Signal Object
        :rtype: StatusSignal[celsius]
        """
        return self._common_lookup(SpnValue.PRO_SUPPLY_AND_TEMP_PROCESSOR_TEMP.value, 0, None, "processor_temp", True, celsius)
    
    def get_rotor_velocity(self) -> StatusSignal[rotations_per_second]:
        """
        Velocity of the motor rotor. This velocity is not affected by any
        feedback configs.
        
            - Minimum Value: -512.0
            - Maximum Value: 511.998046875
            - Default Value: 0
            - Units: rotations per second
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: RotorVelocity Status Signal Object
        :rtype: StatusSignal[rotations_per_second]
        """
        return self._common_lookup(SpnValue.PRO_ROTOR_POS_AND_VEL_VELOCITY.value, 0, None, "rotor_velocity", True, rotations_per_second)
    
    def get_rotor_position(self) -> StatusSignal[rotation]:
        """
        Position of the motor rotor. This position is only affected by the
        RotorOffset config and calls to setPosition.
        
            - Minimum Value: -16384.0
            - Maximum Value: 16383.999755859375
            - Default Value: 0
            - Units: rotations
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: RotorPosition Status Signal Object
        :rtype: StatusSignal[rotation]
        """
        return self._common_lookup(SpnValue.PRO_ROTOR_POS_AND_VEL_POSITION.value, 0, None, "rotor_position", True, rotation)
    
    def get_velocity(self) -> StatusSignal[rotations_per_second]:
        """
        Velocity of the device in mechanism rotations per second. This can be
        the velocity of a remote sensor and is affected by the
        RotorToSensorRatio and SensorToMechanismRatio configs.
        
            - Minimum Value: -512.0
            - Maximum Value: 511.998046875
            - Default Value: 0
            - Units: rotations per second
        
        Default Rates:
            - CAN 2.0: 50.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Velocity Status Signal Object
        :rtype: StatusSignal[rotations_per_second]
        """
        return self._common_lookup(SpnValue.PRO_POS_AND_VEL_VELOCITY.value, 0, None, "velocity", True, rotations_per_second)
    
    def get_position(self) -> StatusSignal[rotation]:
        """
        Position of the device in mechanism rotations. This can be the
        position of a remote sensor and is affected by the RotorToSensorRatio
        and SensorToMechanismRatio configs, as well as calls to setPosition.
        
            - Minimum Value: -16384.0
            - Maximum Value: 16383.999755859375
            - Default Value: 0
            - Units: rotations
        
        Default Rates:
            - CAN 2.0: 50.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Position Status Signal Object
        :rtype: StatusSignal[rotation]
        """
        return self._common_lookup(SpnValue.PRO_POS_AND_VEL_POSITION.value, 0, None, "position", True, rotation)
    
    def get_acceleration(self) -> StatusSignal[rotations_per_second_squared]:
        """
        Acceleration of the device in mechanism rotations per second². This
        can be the acceleration of a remote sensor and is affected by the
        RotorToSensorRatio and SensorToMechanismRatio configs.
        
            - Minimum Value: -2048.0
            - Maximum Value: 2047.75
            - Default Value: 0
            - Units: rotations per second²
        
        Default Rates:
            - CAN 2.0: 50.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Acceleration Status Signal Object
        :rtype: StatusSignal[rotations_per_second_squared]
        """
        return self._common_lookup(SpnValue.PRO_POS_AND_VEL_ACCELERATION.value, 0, None, "acceleration", True, rotations_per_second_squared)
    
    def get_control_mode(self) -> StatusSignal[ControlModeValue]:
        """
        The active control mode of the motor controller
        
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: ControlMode Status Signal Object
        :rtype: StatusSignal[ControlModeValue]
        """
        return self._common_lookup(SpnValue.TALON_FX_CONTROL_MODE.value, 0, None, "control_mode", True, ControlModeValue)
    
    def get_motion_magic_is_running(self) -> StatusSignal[MotionMagicIsRunningValue]:
        """
        Check if Motion Magic® is running.  This is equivalent to checking
        that the reported control mode is a Motion Magic® based mode.
        
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: MotionMagicIsRunning Status Signal Object
        :rtype: StatusSignal[MotionMagicIsRunningValue]
        """
        return self._common_lookup(SpnValue.PRO_PIDSTATE_ENABLES_IS_MOTION_MAGIC_RUNNING.value, 0, None, "motion_magic_is_running", True, MotionMagicIsRunningValue)
    
    def get_device_enable(self) -> StatusSignal[DeviceEnableValue]:
        """
        Indicates if device is actuator enabled.
        
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DeviceEnable Status Signal Object
        :rtype: StatusSignal[DeviceEnableValue]
        """
        return self._common_lookup(SpnValue.PRO_PIDSTATE_ENABLES_DEVICE_ENABLE.value, 0, None, "device_enable", True, DeviceEnableValue)
    
    def get_closed_loop_slot(self) -> StatusSignal[int]:
        """
        Closed loop slot in use
        
        This is the slot that the closed loop PID is using.
        
            - Minimum Value: 0
            - Maximum Value: 2
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: ClosedLoopSlot Status Signal Object
        :rtype: StatusSignal[int]
        """
        return self._common_lookup(SpnValue.PRO_PIDOUTPUT_SLOT.value, 0, None, "closed_loop_slot", True, int)
    
    def get_differential_control_mode(self) -> StatusSignal[DifferentialControlModeValue]:
        """
        The active control mode of the differential controller
        
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialControlMode Status Signal Object
        :rtype: StatusSignal[DifferentialControlModeValue]
        """
        return self._common_lookup(SpnValue.TALON_FX_DIFFERENTIAL_CONTROL_MODE.value, 0, None, "differential_control_mode", True, DifferentialControlModeValue)
    
    def get_differential_average_velocity(self) -> StatusSignal[rotations_per_second]:
        """
        Average component of the differential velocity of device.
        
            - Minimum Value: -512.0
            - Maximum Value: 511.998046875
            - Default Value: 0
            - Units: rotations per second
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialAverageVelocity Status Signal Object
        :rtype: StatusSignal[rotations_per_second]
        """
        return self._common_lookup(SpnValue.PRO_AVG_POS_AND_VEL_VELOCITY.value, 0, None, "differential_average_velocity", True, rotations_per_second)
    
    def get_differential_average_position(self) -> StatusSignal[rotation]:
        """
        Average component of the differential position of device.
        
            - Minimum Value: -16384.0
            - Maximum Value: 16383.999755859375
            - Default Value: 0
            - Units: rotations
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialAveragePosition Status Signal Object
        :rtype: StatusSignal[rotation]
        """
        return self._common_lookup(SpnValue.PRO_AVG_POS_AND_VEL_POSITION.value, 0, None, "differential_average_position", True, rotation)
    
    def get_differential_difference_velocity(self) -> StatusSignal[rotations_per_second]:
        """
        Difference component of the differential velocity of device.
        
            - Minimum Value: -512.0
            - Maximum Value: 511.998046875
            - Default Value: 0
            - Units: rotations per second
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialDifferenceVelocity Status Signal Object
        :rtype: StatusSignal[rotations_per_second]
        """
        return self._common_lookup(SpnValue.PRO_DIFF_POS_AND_VEL_VELOCITY.value, 0, None, "differential_difference_velocity", True, rotations_per_second)
    
    def get_differential_difference_position(self) -> StatusSignal[rotation]:
        """
        Difference component of the differential position of device.
        
            - Minimum Value: -16384.0
            - Maximum Value: 16383.999755859375
            - Default Value: 0
            - Units: rotations
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialDifferencePosition Status Signal Object
        :rtype: StatusSignal[rotation]
        """
        return self._common_lookup(SpnValue.PRO_DIFF_POS_AND_VEL_POSITION.value, 0, None, "differential_difference_position", True, rotation)
    
    def get_differential_closed_loop_slot(self) -> StatusSignal[int]:
        """
        Differential Closed loop slot in use
        
        This is the slot that the closed loop differential PID is using.
        
            - Minimum Value: 0
            - Maximum Value: 2
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: DifferentialClosedLoopSlot Status Signal Object
        :rtype: StatusSignal[int]
        """
        return self._common_lookup(SpnValue.PRO_DIFF_PIDOUTPUT_SLOT.value, 0, None, "differential_closed_loop_slot", True, int)
    
    def get_bridge_output(self) -> StatusSignal[BridgeOutputValue]:
        """
        The applied output of the bridge.
        
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: BridgeOutput Status Signal Object
        :rtype: StatusSignal[BridgeOutputValue]
        """
        return self._common_lookup(SpnValue.PRO_MOTOR_OUTPUT_BRIDGE_TYPE_PUBLIC.value, 0, None, "bridge_output", True, BridgeOutputValue)
    
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
    
    def get_ancillary_device_temp(self) -> StatusSignal[celsius]:
        """
        Temperature of device from second sensor
        
        Newer versions of Talon FX have multiple temperature measurement
        methods.
        
            - Minimum Value: 0.0
            - Maximum Value: 255.0
            - Default Value: 0
            - Units: ℃
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: AncillaryDeviceTemp Status Signal Object
        :rtype: StatusSignal[celsius]
        """
        return self._common_lookup(SpnValue.PRO_SUPPLY_AND_TEMP_DEVICE_TEMP2.value, 0, None, "ancillary_device_temp", True, celsius)
    
    def get_motor_type(self) -> StatusSignal[MotorTypeValue]:
        """
        The type of motor attached to the Talon FX
        
        This can be used to determine what motor is attached to the Talon FX. 
        Return will be "Unknown" if firmware is too old or device is not
        present.
        
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: MotorType Status Signal Object
        :rtype: StatusSignal[MotorTypeValue]
        """
        return self._common_lookup(SpnValue.TALON_FX_MOTOR_TYPE.value, 0, None, "motor_type", True, MotorTypeValue)
    
    def get_motor_output_status(self) -> StatusSignal[MotorOutputStatusValue]:
        """
        Assess the status of the motor output with respect to load and supply.
        
        This routine can be used to determine the general status of motor
        commutation.  Off means that motor output is disabled.  StaticBraking
        typically means the motor is in neutral-brake.  Motoring means motor
        is loaded in a typical fashion, drawing current from the supply, and
        successfully turning the rotor in the direction of applied voltage. 
        Discordant Motoring is the same as Motoring, expect the rotor is being
        backdriven as the motor output is not enough to defeat load forces. 
        RegenBraking means the motor is braking in such a way where motor
        current is traveling back to the supply (typically a battery).
        
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: MotorOutputStatus Status Signal Object
        :rtype: StatusSignal[MotorOutputStatusValue]
        """
        return self._common_lookup(SpnValue.TALON_FX_MOTOR_OUTPUT_STATUS.value, 0, None, "motor_output_status", True, MotorOutputStatusValue)
    
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
    
    def get_fault_proc_temp(self) -> StatusSignal[bool]:
        """
        Processor temperature exceeded limit
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_ProcTemp Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_PROC_TEMP.value, 0, None, "fault_proc_temp", True, bool)
    
    def get_sticky_fault_proc_temp(self) -> StatusSignal[bool]:
        """
        Processor temperature exceeded limit
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_ProcTemp Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_PROC_TEMP.value, 0, None, "sticky_fault_proc_temp", True, bool)
    
    def get_fault_device_temp(self) -> StatusSignal[bool]:
        """
        Device temperature exceeded limit
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_DeviceTemp Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_DEVICE_TEMP.value, 0, None, "fault_device_temp", True, bool)
    
    def get_sticky_fault_device_temp(self) -> StatusSignal[bool]:
        """
        Device temperature exceeded limit
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_DeviceTemp Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_DEVICE_TEMP.value, 0, None, "sticky_fault_device_temp", True, bool)
    
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
    
    def get_fault_bridge_brownout(self) -> StatusSignal[bool]:
        """
        Bridge was disabled most likely due to supply voltage dropping too
        low.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_BridgeBrownout Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_BRIDGE_BROWNOUT.value, 0, None, "fault_bridge_brownout", True, bool)
    
    def get_sticky_fault_bridge_brownout(self) -> StatusSignal[bool]:
        """
        Bridge was disabled most likely due to supply voltage dropping too
        low.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_BridgeBrownout Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_BRIDGE_BROWNOUT.value, 0, None, "sticky_fault_bridge_brownout", True, bool)
    
    def get_fault_remote_sensor_reset(self) -> StatusSignal[bool]:
        """
        The remote sensor has reset.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_RemoteSensorReset Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_REMOTE_SENSOR_RESET.value, 0, None, "fault_remote_sensor_reset", True, bool)
    
    def get_sticky_fault_remote_sensor_reset(self) -> StatusSignal[bool]:
        """
        The remote sensor has reset.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_RemoteSensorReset Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_REMOTE_SENSOR_RESET.value, 0, None, "sticky_fault_remote_sensor_reset", True, bool)
    
    def get_fault_missing_differential_fx(self) -> StatusSignal[bool]:
        """
        The remote Talon FX used for differential control is not present on
        CAN Bus.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_MissingDifferentialFX Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_MISSING_DIFFERENTIAL_FX.value, 0, None, "fault_missing_differential_fx", True, bool)
    
    def get_sticky_fault_missing_differential_fx(self) -> StatusSignal[bool]:
        """
        The remote Talon FX used for differential control is not present on
        CAN Bus.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_MissingDifferentialFX Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_MISSING_DIFFERENTIAL_FX.value, 0, None, "sticky_fault_missing_differential_fx", True, bool)
    
    def get_fault_remote_sensor_pos_overflow(self) -> StatusSignal[bool]:
        """
        The remote sensor position has overflowed. Because of the nature of
        remote sensors, it is possible for the remote sensor position to
        overflow beyond what is supported by the status signal frame. However,
        this is rare and cannot occur over the course of an FRC match under
        normal use.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_RemoteSensorPosOverflow Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_REMOTE_SENSOR_POS_OVERFLOW.value, 0, None, "fault_remote_sensor_pos_overflow", True, bool)
    
    def get_sticky_fault_remote_sensor_pos_overflow(self) -> StatusSignal[bool]:
        """
        The remote sensor position has overflowed. Because of the nature of
        remote sensors, it is possible for the remote sensor position to
        overflow beyond what is supported by the status signal frame. However,
        this is rare and cannot occur over the course of an FRC match under
        normal use.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_RemoteSensorPosOverflow Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_REMOTE_SENSOR_POS_OVERFLOW.value, 0, None, "sticky_fault_remote_sensor_pos_overflow", True, bool)
    
    def get_fault_over_supply_v(self) -> StatusSignal[bool]:
        """
        Supply Voltage has exceeded the maximum voltage rating of device.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_OverSupplyV Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_OVER_SUPPLYV.value, 0, None, "fault_over_supply_v", True, bool)
    
    def get_sticky_fault_over_supply_v(self) -> StatusSignal[bool]:
        """
        Supply Voltage has exceeded the maximum voltage rating of device.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_OverSupplyV Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_OVER_SUPPLYV.value, 0, None, "sticky_fault_over_supply_v", True, bool)
    
    def get_fault_unstable_supply_v(self) -> StatusSignal[bool]:
        """
        Supply Voltage is unstable.  Ensure you are using a battery and
        current limited power supply.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_UnstableSupplyV Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_UNSTABLE_SUPPLYV.value, 0, None, "fault_unstable_supply_v", True, bool)
    
    def get_sticky_fault_unstable_supply_v(self) -> StatusSignal[bool]:
        """
        Supply Voltage is unstable.  Ensure you are using a battery and
        current limited power supply.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_UnstableSupplyV Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_UNSTABLE_SUPPLYV.value, 0, None, "sticky_fault_unstable_supply_v", True, bool)
    
    def get_fault_reverse_hard_limit(self) -> StatusSignal[bool]:
        """
        Reverse limit switch has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_ReverseHardLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_REVERSE_HARD_LIMIT.value, 0, None, "fault_reverse_hard_limit", True, bool)
    
    def get_sticky_fault_reverse_hard_limit(self) -> StatusSignal[bool]:
        """
        Reverse limit switch has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_ReverseHardLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_REVERSE_HARD_LIMIT.value, 0, None, "sticky_fault_reverse_hard_limit", True, bool)
    
    def get_fault_forward_hard_limit(self) -> StatusSignal[bool]:
        """
        Forward limit switch has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_ForwardHardLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_FORWARD_HARD_LIMIT.value, 0, None, "fault_forward_hard_limit", True, bool)
    
    def get_sticky_fault_forward_hard_limit(self) -> StatusSignal[bool]:
        """
        Forward limit switch has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_ForwardHardLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_FORWARD_HARD_LIMIT.value, 0, None, "sticky_fault_forward_hard_limit", True, bool)
    
    def get_fault_reverse_soft_limit(self) -> StatusSignal[bool]:
        """
        Reverse soft limit has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_ReverseSoftLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_REVERSE_SOFT_LIMIT.value, 0, None, "fault_reverse_soft_limit", True, bool)
    
    def get_sticky_fault_reverse_soft_limit(self) -> StatusSignal[bool]:
        """
        Reverse soft limit has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_ReverseSoftLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_REVERSE_SOFT_LIMIT.value, 0, None, "sticky_fault_reverse_soft_limit", True, bool)
    
    def get_fault_forward_soft_limit(self) -> StatusSignal[bool]:
        """
        Forward soft limit has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_ForwardSoftLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_FORWARD_SOFT_LIMIT.value, 0, None, "fault_forward_soft_limit", True, bool)
    
    def get_sticky_fault_forward_soft_limit(self) -> StatusSignal[bool]:
        """
        Forward soft limit has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_ForwardSoftLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_FORWARD_SOFT_LIMIT.value, 0, None, "sticky_fault_forward_soft_limit", True, bool)
    
    def get_fault_remote_sensor_data_invalid(self) -> StatusSignal[bool]:
        """
        The remote sensor's data is no longer trusted. This can happen if the
        remote sensor disappears from the CAN bus or if the remote sensor
        indicates its data is no longer valid, such as when a CANcoder's
        magnet strength falls into the "red" range.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_RemoteSensorDataInvalid Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_MISSING_REMOTE_SENSOR.value, 0, None, "fault_remote_sensor_data_invalid", True, bool)
    
    def get_sticky_fault_remote_sensor_data_invalid(self) -> StatusSignal[bool]:
        """
        The remote sensor's data is no longer trusted. This can happen if the
        remote sensor disappears from the CAN bus or if the remote sensor
        indicates its data is no longer valid, such as when a CANcoder's
        magnet strength falls into the "red" range.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_RemoteSensorDataInvalid Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_MISSING_REMOTE_SENSOR.value, 0, None, "sticky_fault_remote_sensor_data_invalid", True, bool)
    
    def get_fault_fused_sensor_out_of_sync(self) -> StatusSignal[bool]:
        """
        The remote sensor used for fusion has fallen out of sync to the local
        sensor. A re-synchronization has occurred, which may cause a
        discontinuity. This typically happens if there is significant slop in
        the mechanism, or if the RotorToSensorRatio configuration parameter is
        incorrect.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_FusedSensorOutOfSync Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_FUSED_SENSOR_OUT_OF_SYNC.value, 0, None, "fault_fused_sensor_out_of_sync", True, bool)
    
    def get_sticky_fault_fused_sensor_out_of_sync(self) -> StatusSignal[bool]:
        """
        The remote sensor used for fusion has fallen out of sync to the local
        sensor. A re-synchronization has occurred, which may cause a
        discontinuity. This typically happens if there is significant slop in
        the mechanism, or if the RotorToSensorRatio configuration parameter is
        incorrect.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_FusedSensorOutOfSync Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_FUSED_SENSOR_OUT_OF_SYNC.value, 0, None, "sticky_fault_fused_sensor_out_of_sync", True, bool)
    
    def get_fault_stator_curr_limit(self) -> StatusSignal[bool]:
        """
        Stator current limit occured.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_StatorCurrLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_STATOR_CURR_LIMIT.value, 0, None, "fault_stator_curr_limit", True, bool)
    
    def get_sticky_fault_stator_curr_limit(self) -> StatusSignal[bool]:
        """
        Stator current limit occured.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_StatorCurrLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_STATOR_CURR_LIMIT.value, 0, None, "sticky_fault_stator_curr_limit", True, bool)
    
    def get_fault_supply_curr_limit(self) -> StatusSignal[bool]:
        """
        Supply current limit occured.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_SupplyCurrLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_SUPPLY_CURR_LIMIT.value, 0, None, "fault_supply_curr_limit", True, bool)
    
    def get_sticky_fault_supply_curr_limit(self) -> StatusSignal[bool]:
        """
        Supply current limit occured.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_SupplyCurrLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_SUPPLY_CURR_LIMIT.value, 0, None, "sticky_fault_supply_curr_limit", True, bool)
    
    def get_fault_using_fused_ca_ncoder_while_unlicensed(self) -> StatusSignal[bool]:
        """
        Using Fused CANcoder feature while unlicensed. Device has fallen back
        to remote CANcoder.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_UsingFusedCANcoderWhileUnlicensed Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_USING_FUSED_CCWHILE_UNLICENSED.value, 0, None, "fault_using_fused_ca_ncoder_while_unlicensed", True, bool)
    
    def get_sticky_fault_using_fused_ca_ncoder_while_unlicensed(self) -> StatusSignal[bool]:
        """
        Using Fused CANcoder feature while unlicensed. Device has fallen back
        to remote CANcoder.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_UsingFusedCANcoderWhileUnlicensed Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_USING_FUSED_CCWHILE_UNLICENSED.value, 0, None, "sticky_fault_using_fused_ca_ncoder_while_unlicensed", True, bool)
    
    def get_fault_static_brake_disabled(self) -> StatusSignal[bool]:
        """
        Static brake was momentarily disabled due to excessive braking current
        while disabled.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: Fault_StaticBrakeDisabled Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_STATIC_BRAKE_DISABLED.value, 0, None, "fault_static_brake_disabled", True, bool)
    
    def get_sticky_fault_static_brake_disabled(self) -> StatusSignal[bool]:
        """
        Static brake was momentarily disabled due to excessive braking current
        while disabled.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns: StickyFault_StaticBrakeDisabled Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_STATIC_BRAKE_DISABLED.value, 0, None, "sticky_fault_static_brake_disabled", True, bool)
    
    def get_closed_loop_proportional_output(self) -> StatusSignal[float]:
        """
        Closed loop proportional component
        
        The portion of the closed loop output that is the proportional to the
        error. Alternatively, the p-Contribution of the closed loop output.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns:  ClosedLoopProportionalOutput Status Signal object
        """
        map_filler = lambda: {
            ControlModeValue.POSITION_DUTY_CYCLE.value: self._get_pid_duty_cycle_proportional_output(),
            ControlModeValue.POSITION_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_proportional_output(),
            ControlModeValue.VELOCITY_DUTY_CYCLE.value: self._get_pid_duty_cycle_proportional_output(),
            ControlModeValue.VELOCITY_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_proportional_output(),
            ControlModeValue.MOTION_MAGIC_DUTY_CYCLE.value: self._get_pid_duty_cycle_proportional_output(),
            ControlModeValue.MOTION_MAGIC_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_proportional_output(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_DUTY_CYCLE.value: self._get_pid_duty_cycle_proportional_output(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_proportional_output(),
            ControlModeValue.MOTION_MAGIC_EXPO_DUTY_CYCLE.value: self._get_pid_duty_cycle_proportional_output(),
            ControlModeValue.MOTION_MAGIC_EXPO_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_proportional_output(),
            ControlModeValue.POSITION_VOLTAGE.value: self._get_pid_motor_voltage_proportional_output(),
            ControlModeValue.POSITION_VOLTAGE_FOC.value: self._get_pid_motor_voltage_proportional_output(),
            ControlModeValue.VELOCITY_VOLTAGE.value: self._get_pid_motor_voltage_proportional_output(),
            ControlModeValue.VELOCITY_VOLTAGE_FOC.value: self._get_pid_motor_voltage_proportional_output(),
            ControlModeValue.MOTION_MAGIC_VOLTAGE.value: self._get_pid_motor_voltage_proportional_output(),
            ControlModeValue.MOTION_MAGIC_VOLTAGE_FOC.value: self._get_pid_motor_voltage_proportional_output(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_VOLTAGE.value: self._get_pid_motor_voltage_proportional_output(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_VOLTAGE_FOC.value: self._get_pid_motor_voltage_proportional_output(),
            ControlModeValue.MOTION_MAGIC_EXPO_VOLTAGE.value: self._get_pid_motor_voltage_proportional_output(),
            ControlModeValue.MOTION_MAGIC_EXPO_VOLTAGE_FOC.value: self._get_pid_motor_voltage_proportional_output(),
            ControlModeValue.POSITION_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_proportional_output(),
            ControlModeValue.VELOCITY_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_proportional_output(),
            ControlModeValue.MOTION_MAGIC_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_proportional_output(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_proportional_output(),
            ControlModeValue.MOTION_MAGIC_EXPO_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_proportional_output(),
        }
        return self._common_lookup(SpnValue.TALON_FX_CONTROL_MODE.value, 1, map_filler, "closed_loop_proportional_output", True, float)
    
    def get_closed_loop_integrated_output(self) -> StatusSignal[float]:
        """
        Closed loop integrated component
        
        The portion of the closed loop output that is proportional to the
        integrated error. Alternatively, the i-Contribution of the closed loop
        output.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns:  ClosedLoopIntegratedOutput Status Signal object
        """
        map_filler = lambda: {
            ControlModeValue.POSITION_DUTY_CYCLE.value: self._get_pid_duty_cycle_integrated_accum(),
            ControlModeValue.POSITION_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_integrated_accum(),
            ControlModeValue.VELOCITY_DUTY_CYCLE.value: self._get_pid_duty_cycle_integrated_accum(),
            ControlModeValue.VELOCITY_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_integrated_accum(),
            ControlModeValue.MOTION_MAGIC_DUTY_CYCLE.value: self._get_pid_duty_cycle_integrated_accum(),
            ControlModeValue.MOTION_MAGIC_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_integrated_accum(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_DUTY_CYCLE.value: self._get_pid_duty_cycle_integrated_accum(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_integrated_accum(),
            ControlModeValue.MOTION_MAGIC_EXPO_DUTY_CYCLE.value: self._get_pid_duty_cycle_integrated_accum(),
            ControlModeValue.MOTION_MAGIC_EXPO_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_integrated_accum(),
            ControlModeValue.POSITION_VOLTAGE.value: self._get_pid_motor_voltage_integrated_accum(),
            ControlModeValue.POSITION_VOLTAGE_FOC.value: self._get_pid_motor_voltage_integrated_accum(),
            ControlModeValue.VELOCITY_VOLTAGE.value: self._get_pid_motor_voltage_integrated_accum(),
            ControlModeValue.VELOCITY_VOLTAGE_FOC.value: self._get_pid_motor_voltage_integrated_accum(),
            ControlModeValue.MOTION_MAGIC_VOLTAGE.value: self._get_pid_motor_voltage_integrated_accum(),
            ControlModeValue.MOTION_MAGIC_VOLTAGE_FOC.value: self._get_pid_motor_voltage_integrated_accum(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_VOLTAGE.value: self._get_pid_motor_voltage_integrated_accum(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_VOLTAGE_FOC.value: self._get_pid_motor_voltage_integrated_accum(),
            ControlModeValue.MOTION_MAGIC_EXPO_VOLTAGE.value: self._get_pid_motor_voltage_integrated_accum(),
            ControlModeValue.MOTION_MAGIC_EXPO_VOLTAGE_FOC.value: self._get_pid_motor_voltage_integrated_accum(),
            ControlModeValue.POSITION_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_integrated_accum(),
            ControlModeValue.VELOCITY_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_integrated_accum(),
            ControlModeValue.MOTION_MAGIC_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_integrated_accum(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_integrated_accum(),
            ControlModeValue.MOTION_MAGIC_EXPO_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_integrated_accum(),
        }
        return self._common_lookup(SpnValue.TALON_FX_CONTROL_MODE.value, 2, map_filler, "closed_loop_integrated_output", True, float)
    
    def get_closed_loop_feed_forward(self) -> StatusSignal[float]:
        """
        Feedforward passed by the user
        
        This is the general feedforward that the user provides for the closed
        loop.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns:  ClosedLoopFeedForward Status Signal object
        """
        map_filler = lambda: {
            ControlModeValue.POSITION_DUTY_CYCLE.value: self._get_pid_duty_cycle_feed_forward(),
            ControlModeValue.POSITION_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_feed_forward(),
            ControlModeValue.VELOCITY_DUTY_CYCLE.value: self._get_pid_duty_cycle_feed_forward(),
            ControlModeValue.VELOCITY_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_feed_forward(),
            ControlModeValue.MOTION_MAGIC_DUTY_CYCLE.value: self._get_pid_duty_cycle_feed_forward(),
            ControlModeValue.MOTION_MAGIC_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_feed_forward(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_DUTY_CYCLE.value: self._get_pid_duty_cycle_feed_forward(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_feed_forward(),
            ControlModeValue.MOTION_MAGIC_EXPO_DUTY_CYCLE.value: self._get_pid_duty_cycle_feed_forward(),
            ControlModeValue.MOTION_MAGIC_EXPO_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_feed_forward(),
            ControlModeValue.POSITION_VOLTAGE.value: self._get_pid_motor_voltage_feed_forward(),
            ControlModeValue.POSITION_VOLTAGE_FOC.value: self._get_pid_motor_voltage_feed_forward(),
            ControlModeValue.VELOCITY_VOLTAGE.value: self._get_pid_motor_voltage_feed_forward(),
            ControlModeValue.VELOCITY_VOLTAGE_FOC.value: self._get_pid_motor_voltage_feed_forward(),
            ControlModeValue.MOTION_MAGIC_VOLTAGE.value: self._get_pid_motor_voltage_feed_forward(),
            ControlModeValue.MOTION_MAGIC_VOLTAGE_FOC.value: self._get_pid_motor_voltage_feed_forward(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_VOLTAGE.value: self._get_pid_motor_voltage_feed_forward(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_VOLTAGE_FOC.value: self._get_pid_motor_voltage_feed_forward(),
            ControlModeValue.MOTION_MAGIC_EXPO_VOLTAGE.value: self._get_pid_motor_voltage_feed_forward(),
            ControlModeValue.MOTION_MAGIC_EXPO_VOLTAGE_FOC.value: self._get_pid_motor_voltage_feed_forward(),
            ControlModeValue.POSITION_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_feed_forward(),
            ControlModeValue.VELOCITY_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_feed_forward(),
            ControlModeValue.MOTION_MAGIC_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_feed_forward(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_feed_forward(),
            ControlModeValue.MOTION_MAGIC_EXPO_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_feed_forward(),
        }
        return self._common_lookup(SpnValue.TALON_FX_CONTROL_MODE.value, 3, map_filler, "closed_loop_feed_forward", True, float)
    
    def get_closed_loop_derivative_output(self) -> StatusSignal[float]:
        """
        Closed loop derivative component
        
        The portion of the closed loop output that is the proportional to the
        deriviative the error. Alternatively, the d-Contribution of the closed
        loop output.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns:  ClosedLoopDerivativeOutput Status Signal object
        """
        map_filler = lambda: {
            ControlModeValue.POSITION_DUTY_CYCLE.value: self._get_pid_duty_cycle_derivative_output(),
            ControlModeValue.POSITION_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_derivative_output(),
            ControlModeValue.VELOCITY_DUTY_CYCLE.value: self._get_pid_duty_cycle_derivative_output(),
            ControlModeValue.VELOCITY_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_derivative_output(),
            ControlModeValue.MOTION_MAGIC_DUTY_CYCLE.value: self._get_pid_duty_cycle_derivative_output(),
            ControlModeValue.MOTION_MAGIC_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_derivative_output(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_DUTY_CYCLE.value: self._get_pid_duty_cycle_derivative_output(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_derivative_output(),
            ControlModeValue.MOTION_MAGIC_EXPO_DUTY_CYCLE.value: self._get_pid_duty_cycle_derivative_output(),
            ControlModeValue.MOTION_MAGIC_EXPO_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_derivative_output(),
            ControlModeValue.POSITION_VOLTAGE.value: self._get_pid_motor_voltage_derivative_output(),
            ControlModeValue.POSITION_VOLTAGE_FOC.value: self._get_pid_motor_voltage_derivative_output(),
            ControlModeValue.VELOCITY_VOLTAGE.value: self._get_pid_motor_voltage_derivative_output(),
            ControlModeValue.VELOCITY_VOLTAGE_FOC.value: self._get_pid_motor_voltage_derivative_output(),
            ControlModeValue.MOTION_MAGIC_VOLTAGE.value: self._get_pid_motor_voltage_derivative_output(),
            ControlModeValue.MOTION_MAGIC_VOLTAGE_FOC.value: self._get_pid_motor_voltage_derivative_output(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_VOLTAGE.value: self._get_pid_motor_voltage_derivative_output(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_VOLTAGE_FOC.value: self._get_pid_motor_voltage_derivative_output(),
            ControlModeValue.MOTION_MAGIC_EXPO_VOLTAGE.value: self._get_pid_motor_voltage_derivative_output(),
            ControlModeValue.MOTION_MAGIC_EXPO_VOLTAGE_FOC.value: self._get_pid_motor_voltage_derivative_output(),
            ControlModeValue.POSITION_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_derivative_output(),
            ControlModeValue.VELOCITY_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_derivative_output(),
            ControlModeValue.MOTION_MAGIC_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_derivative_output(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_derivative_output(),
            ControlModeValue.MOTION_MAGIC_EXPO_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_derivative_output(),
        }
        return self._common_lookup(SpnValue.TALON_FX_CONTROL_MODE.value, 4, map_filler, "closed_loop_derivative_output", True, float)
    
    def get_closed_loop_output(self) -> StatusSignal[float]:
        """
        Closed loop total output
        
        The total output of the closed loop output.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns:  ClosedLoopOutput Status Signal object
        """
        map_filler = lambda: {
            ControlModeValue.POSITION_DUTY_CYCLE.value: self._get_pid_duty_cycle_output(),
            ControlModeValue.POSITION_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_output(),
            ControlModeValue.VELOCITY_DUTY_CYCLE.value: self._get_pid_duty_cycle_output(),
            ControlModeValue.VELOCITY_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_output(),
            ControlModeValue.MOTION_MAGIC_DUTY_CYCLE.value: self._get_pid_duty_cycle_output(),
            ControlModeValue.MOTION_MAGIC_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_output(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_DUTY_CYCLE.value: self._get_pid_duty_cycle_output(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_output(),
            ControlModeValue.MOTION_MAGIC_EXPO_DUTY_CYCLE.value: self._get_pid_duty_cycle_output(),
            ControlModeValue.MOTION_MAGIC_EXPO_DUTY_CYCLE_FOC.value: self._get_pid_duty_cycle_output(),
            ControlModeValue.POSITION_VOLTAGE.value: self._get_pid_motor_voltage_output(),
            ControlModeValue.POSITION_VOLTAGE_FOC.value: self._get_pid_motor_voltage_output(),
            ControlModeValue.VELOCITY_VOLTAGE.value: self._get_pid_motor_voltage_output(),
            ControlModeValue.VELOCITY_VOLTAGE_FOC.value: self._get_pid_motor_voltage_output(),
            ControlModeValue.MOTION_MAGIC_VOLTAGE.value: self._get_pid_motor_voltage_output(),
            ControlModeValue.MOTION_MAGIC_VOLTAGE_FOC.value: self._get_pid_motor_voltage_output(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_VOLTAGE.value: self._get_pid_motor_voltage_output(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_VOLTAGE_FOC.value: self._get_pid_motor_voltage_output(),
            ControlModeValue.MOTION_MAGIC_EXPO_VOLTAGE.value: self._get_pid_motor_voltage_output(),
            ControlModeValue.MOTION_MAGIC_EXPO_VOLTAGE_FOC.value: self._get_pid_motor_voltage_output(),
            ControlModeValue.POSITION_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_output(),
            ControlModeValue.VELOCITY_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_output(),
            ControlModeValue.MOTION_MAGIC_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_output(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_output(),
            ControlModeValue.MOTION_MAGIC_EXPO_TORQUE_CURRENT_FOC.value: self._get_pid_torque_current_output(),
        }
        return self._common_lookup(SpnValue.TALON_FX_CONTROL_MODE.value, 5, map_filler, "closed_loop_output", True, float)
    
    def get_closed_loop_reference(self) -> StatusSignal[float]:
        """
        Value that the closed loop is targeting
        
        This is the value that the closed loop PID controller targets.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns:  ClosedLoopReference Status Signal object
        """
        map_filler = lambda: {
            ControlModeValue.POSITION_DUTY_CYCLE.value: self._get_pid_position_reference(),
            ControlModeValue.POSITION_DUTY_CYCLE_FOC.value: self._get_pid_position_reference(),
            ControlModeValue.MOTION_MAGIC_DUTY_CYCLE.value: self._get_pid_position_reference(),
            ControlModeValue.MOTION_MAGIC_DUTY_CYCLE_FOC.value: self._get_pid_position_reference(),
            ControlModeValue.POSITION_VOLTAGE.value: self._get_pid_position_reference(),
            ControlModeValue.POSITION_VOLTAGE_FOC.value: self._get_pid_position_reference(),
            ControlModeValue.MOTION_MAGIC_VOLTAGE.value: self._get_pid_position_reference(),
            ControlModeValue.MOTION_MAGIC_VOLTAGE_FOC.value: self._get_pid_position_reference(),
            ControlModeValue.POSITION_TORQUE_CURRENT_FOC.value: self._get_pid_position_reference(),
            ControlModeValue.MOTION_MAGIC_TORQUE_CURRENT_FOC.value: self._get_pid_position_reference(),
            ControlModeValue.MOTION_MAGIC_EXPO_DUTY_CYCLE.value: self._get_pid_position_reference(),
            ControlModeValue.MOTION_MAGIC_EXPO_DUTY_CYCLE_FOC.value: self._get_pid_position_reference(),
            ControlModeValue.MOTION_MAGIC_EXPO_VOLTAGE.value: self._get_pid_position_reference(),
            ControlModeValue.MOTION_MAGIC_EXPO_VOLTAGE_FOC.value: self._get_pid_position_reference(),
            ControlModeValue.MOTION_MAGIC_EXPO_TORQUE_CURRENT_FOC.value: self._get_pid_position_reference(),
            ControlModeValue.VELOCITY_DUTY_CYCLE.value: self._get_pid_velocity_reference(),
            ControlModeValue.VELOCITY_DUTY_CYCLE_FOC.value: self._get_pid_velocity_reference(),
            ControlModeValue.VELOCITY_VOLTAGE.value: self._get_pid_velocity_reference(),
            ControlModeValue.VELOCITY_VOLTAGE_FOC.value: self._get_pid_velocity_reference(),
            ControlModeValue.VELOCITY_TORQUE_CURRENT_FOC.value: self._get_pid_velocity_reference(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_DUTY_CYCLE.value: self._get_pid_velocity_reference(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_DUTY_CYCLE_FOC.value: self._get_pid_velocity_reference(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_VOLTAGE.value: self._get_pid_velocity_reference(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_VOLTAGE_FOC.value: self._get_pid_velocity_reference(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_TORQUE_CURRENT_FOC.value: self._get_pid_velocity_reference(),
        }
        return self._common_lookup(SpnValue.TALON_FX_CONTROL_MODE.value, 6, map_filler, "closed_loop_reference", True, float)
    
    def get_closed_loop_reference_slope(self) -> StatusSignal[float]:
        """
        Derivative of the target that the closed loop is targeting
        
        This is the change in the closed loop reference. This may be used in
        the feed-forward calculation, the derivative-error, or in application
        of the signage for kS. Typically, this represents the target velocity
        during Motion Magic®.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns:  ClosedLoopReferenceSlope Status Signal object
        """
        map_filler = lambda: {
            ControlModeValue.POSITION_DUTY_CYCLE.value: self._get_pid_position_reference_slope(),
            ControlModeValue.POSITION_DUTY_CYCLE_FOC.value: self._get_pid_position_reference_slope(),
            ControlModeValue.MOTION_MAGIC_DUTY_CYCLE.value: self._get_pid_position_reference_slope(),
            ControlModeValue.MOTION_MAGIC_DUTY_CYCLE_FOC.value: self._get_pid_position_reference_slope(),
            ControlModeValue.POSITION_VOLTAGE.value: self._get_pid_position_reference_slope(),
            ControlModeValue.POSITION_VOLTAGE_FOC.value: self._get_pid_position_reference_slope(),
            ControlModeValue.MOTION_MAGIC_VOLTAGE.value: self._get_pid_position_reference_slope(),
            ControlModeValue.MOTION_MAGIC_VOLTAGE_FOC.value: self._get_pid_position_reference_slope(),
            ControlModeValue.POSITION_TORQUE_CURRENT_FOC.value: self._get_pid_position_reference_slope(),
            ControlModeValue.MOTION_MAGIC_TORQUE_CURRENT_FOC.value: self._get_pid_position_reference_slope(),
            ControlModeValue.MOTION_MAGIC_EXPO_DUTY_CYCLE.value: self._get_pid_position_reference_slope(),
            ControlModeValue.MOTION_MAGIC_EXPO_DUTY_CYCLE_FOC.value: self._get_pid_position_reference_slope(),
            ControlModeValue.MOTION_MAGIC_EXPO_VOLTAGE.value: self._get_pid_position_reference_slope(),
            ControlModeValue.MOTION_MAGIC_EXPO_VOLTAGE_FOC.value: self._get_pid_position_reference_slope(),
            ControlModeValue.MOTION_MAGIC_EXPO_TORQUE_CURRENT_FOC.value: self._get_pid_position_reference_slope(),
            ControlModeValue.VELOCITY_DUTY_CYCLE.value: self._get_pid_velocity_reference_slope(),
            ControlModeValue.VELOCITY_DUTY_CYCLE_FOC.value: self._get_pid_velocity_reference_slope(),
            ControlModeValue.VELOCITY_VOLTAGE.value: self._get_pid_velocity_reference_slope(),
            ControlModeValue.VELOCITY_VOLTAGE_FOC.value: self._get_pid_velocity_reference_slope(),
            ControlModeValue.VELOCITY_TORQUE_CURRENT_FOC.value: self._get_pid_velocity_reference_slope(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_DUTY_CYCLE.value: self._get_pid_velocity_reference_slope(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_DUTY_CYCLE_FOC.value: self._get_pid_velocity_reference_slope(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_VOLTAGE.value: self._get_pid_velocity_reference_slope(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_VOLTAGE_FOC.value: self._get_pid_velocity_reference_slope(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_TORQUE_CURRENT_FOC.value: self._get_pid_velocity_reference_slope(),
        }
        return self._common_lookup(SpnValue.TALON_FX_CONTROL_MODE.value, 7, map_filler, "closed_loop_reference_slope", True, float)
    
    def get_closed_loop_error(self) -> StatusSignal[float]:
        """
        The difference between target reference and current measurement
        
        This is the value that is treated as the error in the PID loop.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns:  ClosedLoopError Status Signal object
        """
        map_filler = lambda: {
            ControlModeValue.POSITION_DUTY_CYCLE.value: self._get_pid_position_closed_loop_error(),
            ControlModeValue.POSITION_DUTY_CYCLE_FOC.value: self._get_pid_position_closed_loop_error(),
            ControlModeValue.MOTION_MAGIC_DUTY_CYCLE.value: self._get_pid_position_closed_loop_error(),
            ControlModeValue.MOTION_MAGIC_DUTY_CYCLE_FOC.value: self._get_pid_position_closed_loop_error(),
            ControlModeValue.POSITION_VOLTAGE.value: self._get_pid_position_closed_loop_error(),
            ControlModeValue.POSITION_VOLTAGE_FOC.value: self._get_pid_position_closed_loop_error(),
            ControlModeValue.MOTION_MAGIC_VOLTAGE.value: self._get_pid_position_closed_loop_error(),
            ControlModeValue.MOTION_MAGIC_VOLTAGE_FOC.value: self._get_pid_position_closed_loop_error(),
            ControlModeValue.POSITION_TORQUE_CURRENT_FOC.value: self._get_pid_position_closed_loop_error(),
            ControlModeValue.MOTION_MAGIC_TORQUE_CURRENT_FOC.value: self._get_pid_position_closed_loop_error(),
            ControlModeValue.MOTION_MAGIC_EXPO_DUTY_CYCLE.value: self._get_pid_position_closed_loop_error(),
            ControlModeValue.MOTION_MAGIC_EXPO_DUTY_CYCLE_FOC.value: self._get_pid_position_closed_loop_error(),
            ControlModeValue.MOTION_MAGIC_EXPO_VOLTAGE.value: self._get_pid_position_closed_loop_error(),
            ControlModeValue.MOTION_MAGIC_EXPO_VOLTAGE_FOC.value: self._get_pid_position_closed_loop_error(),
            ControlModeValue.MOTION_MAGIC_EXPO_TORQUE_CURRENT_FOC.value: self._get_pid_position_closed_loop_error(),
            ControlModeValue.VELOCITY_DUTY_CYCLE.value: self._get_pid_velocity_closed_loop_error(),
            ControlModeValue.VELOCITY_DUTY_CYCLE_FOC.value: self._get_pid_velocity_closed_loop_error(),
            ControlModeValue.VELOCITY_VOLTAGE.value: self._get_pid_velocity_closed_loop_error(),
            ControlModeValue.VELOCITY_VOLTAGE_FOC.value: self._get_pid_velocity_closed_loop_error(),
            ControlModeValue.VELOCITY_TORQUE_CURRENT_FOC.value: self._get_pid_velocity_closed_loop_error(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_DUTY_CYCLE.value: self._get_pid_velocity_closed_loop_error(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_DUTY_CYCLE_FOC.value: self._get_pid_velocity_closed_loop_error(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_VOLTAGE.value: self._get_pid_velocity_closed_loop_error(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_VOLTAGE_FOC.value: self._get_pid_velocity_closed_loop_error(),
            ControlModeValue.MOTION_MAGIC_VELOCITY_TORQUE_CURRENT_FOC.value: self._get_pid_velocity_closed_loop_error(),
        }
        return self._common_lookup(SpnValue.TALON_FX_CONTROL_MODE.value, 8, map_filler, "closed_loop_error", True, float)
    
    def get_differential_output(self) -> StatusSignal[float]:
        """
        The calculated motor output for differential followers.
        
        This is a torque request when using the TorqueCurrentFOC control
        output type, and a duty cycle in all other control types.
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns:  DifferentialOutput Status Signal object
        """
        map_filler = lambda: {
            DifferentialControlModeValue.POSITION_DUTY_CYCLE.value: self._get_differential_duty_cycle(),
            DifferentialControlModeValue.POSITION_DUTY_CYCLE_FOC.value: self._get_differential_duty_cycle(),
            DifferentialControlModeValue.MOTION_MAGIC_DUTY_CYCLE.value: self._get_differential_duty_cycle(),
            DifferentialControlModeValue.MOTION_MAGIC_DUTY_CYCLE_FOC.value: self._get_differential_duty_cycle(),
            DifferentialControlModeValue.POSITION_VOLTAGE.value: self._get_differential_duty_cycle(),
            DifferentialControlModeValue.POSITION_VOLTAGE_FOC.value: self._get_differential_duty_cycle(),
            DifferentialControlModeValue.MOTION_MAGIC_VOLTAGE.value: self._get_differential_duty_cycle(),
            DifferentialControlModeValue.MOTION_MAGIC_VOLTAGE_FOC.value: self._get_differential_duty_cycle(),
            DifferentialControlModeValue.VELOCITY_DUTY_CYCLE.value: self._get_differential_duty_cycle(),
            DifferentialControlModeValue.VELOCITY_DUTY_CYCLE_FOC.value: self._get_differential_duty_cycle(),
            DifferentialControlModeValue.VELOCITY_VOLTAGE.value: self._get_differential_duty_cycle(),
            DifferentialControlModeValue.VELOCITY_VOLTAGE_FOC.value: self._get_differential_duty_cycle(),
            DifferentialControlModeValue.POSITION_TORQUE_CURRENT_FOC.value: self._get_differential_torque_current(),
            DifferentialControlModeValue.MOTION_MAGIC_TORQUE_CURRENT_FOC.value: self._get_differential_torque_current(),
            DifferentialControlModeValue.VELOCITY_TORQUE_CURRENT_FOC.value: self._get_differential_torque_current(),
        }
        return self._common_lookup(SpnValue.TALON_FX_DIFFERENTIAL_CONTROL_MODE.value, 9, map_filler, "differential_output", True, float)
    
    def get_differential_closed_loop_proportional_output(self) -> StatusSignal[float]:
        """
        Differential closed loop proportional component
        
        The portion of the differential closed loop output that is the
        proportional to the error. Alternatively, the p-Contribution of the
        closed loop output.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns:  DifferentialClosedLoopProportionalOutput Status Signal object
        """
        map_filler = lambda: {
            DifferentialControlModeValue.POSITION_DUTY_CYCLE.value: self._get_differential_pid_duty_cycle_proportional_output(),
            DifferentialControlModeValue.POSITION_DUTY_CYCLE_FOC.value: self._get_differential_pid_duty_cycle_proportional_output(),
            DifferentialControlModeValue.VELOCITY_DUTY_CYCLE.value: self._get_differential_pid_duty_cycle_proportional_output(),
            DifferentialControlModeValue.VELOCITY_DUTY_CYCLE_FOC.value: self._get_differential_pid_duty_cycle_proportional_output(),
            DifferentialControlModeValue.MOTION_MAGIC_DUTY_CYCLE.value: self._get_differential_pid_duty_cycle_proportional_output(),
            DifferentialControlModeValue.MOTION_MAGIC_DUTY_CYCLE_FOC.value: self._get_differential_pid_duty_cycle_proportional_output(),
            DifferentialControlModeValue.POSITION_VOLTAGE.value: self._get_differential_pid_motor_voltage_proportional_output(),
            DifferentialControlModeValue.POSITION_VOLTAGE_FOC.value: self._get_differential_pid_motor_voltage_proportional_output(),
            DifferentialControlModeValue.VELOCITY_VOLTAGE.value: self._get_differential_pid_motor_voltage_proportional_output(),
            DifferentialControlModeValue.VELOCITY_VOLTAGE_FOC.value: self._get_differential_pid_motor_voltage_proportional_output(),
            DifferentialControlModeValue.MOTION_MAGIC_VOLTAGE.value: self._get_differential_pid_motor_voltage_proportional_output(),
            DifferentialControlModeValue.MOTION_MAGIC_VOLTAGE_FOC.value: self._get_differential_pid_motor_voltage_proportional_output(),
            DifferentialControlModeValue.POSITION_TORQUE_CURRENT_FOC.value: self._get_differential_pid_torque_current_proportional_output(),
            DifferentialControlModeValue.VELOCITY_TORQUE_CURRENT_FOC.value: self._get_differential_pid_torque_current_proportional_output(),
            DifferentialControlModeValue.MOTION_MAGIC_TORQUE_CURRENT_FOC.value: self._get_differential_pid_torque_current_proportional_output(),
        }
        return self._common_lookup(SpnValue.TALON_FX_DIFFERENTIAL_CONTROL_MODE.value, 10, map_filler, "differential_closed_loop_proportional_output", True, float)
    
    def get_differential_closed_loop_integrated_output(self) -> StatusSignal[float]:
        """
        Differential closed loop integrated component
        
        The portion of the differential closed loop output that is
        proportional to the integrated error. Alternatively, the
        i-Contribution of the closed loop output.
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns:  DifferentialClosedLoopIntegratedOutput Status Signal object
        """
        map_filler = lambda: {
            DifferentialControlModeValue.POSITION_DUTY_CYCLE.value: self._get_differential_pid_duty_cycle_integrated_accum(),
            DifferentialControlModeValue.POSITION_DUTY_CYCLE_FOC.value: self._get_differential_pid_duty_cycle_integrated_accum(),
            DifferentialControlModeValue.VELOCITY_DUTY_CYCLE.value: self._get_differential_pid_duty_cycle_integrated_accum(),
            DifferentialControlModeValue.VELOCITY_DUTY_CYCLE_FOC.value: self._get_differential_pid_duty_cycle_integrated_accum(),
            DifferentialControlModeValue.MOTION_MAGIC_DUTY_CYCLE.value: self._get_differential_pid_duty_cycle_integrated_accum(),
            DifferentialControlModeValue.MOTION_MAGIC_DUTY_CYCLE_FOC.value: self._get_differential_pid_duty_cycle_integrated_accum(),
            DifferentialControlModeValue.POSITION_VOLTAGE.value: self._get_differential_pid_motor_voltage_integrated_accum(),
            DifferentialControlModeValue.POSITION_VOLTAGE_FOC.value: self._get_differential_pid_motor_voltage_integrated_accum(),
            DifferentialControlModeValue.VELOCITY_VOLTAGE.value: self._get_differential_pid_motor_voltage_integrated_accum(),
            DifferentialControlModeValue.VELOCITY_VOLTAGE_FOC.value: self._get_differential_pid_motor_voltage_integrated_accum(),
            DifferentialControlModeValue.MOTION_MAGIC_VOLTAGE.value: self._get_differential_pid_motor_voltage_integrated_accum(),
            DifferentialControlModeValue.MOTION_MAGIC_VOLTAGE_FOC.value: self._get_differential_pid_motor_voltage_integrated_accum(),
            DifferentialControlModeValue.POSITION_TORQUE_CURRENT_FOC.value: self._get_differential_pid_torque_current_integrated_accum(),
            DifferentialControlModeValue.VELOCITY_TORQUE_CURRENT_FOC.value: self._get_differential_pid_torque_current_integrated_accum(),
            DifferentialControlModeValue.MOTION_MAGIC_TORQUE_CURRENT_FOC.value: self._get_differential_pid_torque_current_integrated_accum(),
        }
        return self._common_lookup(SpnValue.TALON_FX_DIFFERENTIAL_CONTROL_MODE.value, 11, map_filler, "differential_closed_loop_integrated_output", True, float)
    
    def get_differential_closed_loop_feed_forward(self) -> StatusSignal[float]:
        """
        Differential Feedforward passed by the user
        
        This is the general feedforward that the user provides for the
        differential closed loop.
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns:  DifferentialClosedLoopFeedForward Status Signal object
        """
        map_filler = lambda: {
            DifferentialControlModeValue.POSITION_DUTY_CYCLE.value: self._get_differential_pid_duty_cycle_feed_forward(),
            DifferentialControlModeValue.POSITION_DUTY_CYCLE_FOC.value: self._get_differential_pid_duty_cycle_feed_forward(),
            DifferentialControlModeValue.VELOCITY_DUTY_CYCLE.value: self._get_differential_pid_duty_cycle_feed_forward(),
            DifferentialControlModeValue.VELOCITY_DUTY_CYCLE_FOC.value: self._get_differential_pid_duty_cycle_feed_forward(),
            DifferentialControlModeValue.MOTION_MAGIC_DUTY_CYCLE.value: self._get_differential_pid_duty_cycle_feed_forward(),
            DifferentialControlModeValue.MOTION_MAGIC_DUTY_CYCLE_FOC.value: self._get_differential_pid_duty_cycle_feed_forward(),
            DifferentialControlModeValue.POSITION_VOLTAGE.value: self._get_differential_pid_motor_voltage_feed_forward(),
            DifferentialControlModeValue.POSITION_VOLTAGE_FOC.value: self._get_differential_pid_motor_voltage_feed_forward(),
            DifferentialControlModeValue.VELOCITY_VOLTAGE.value: self._get_differential_pid_motor_voltage_feed_forward(),
            DifferentialControlModeValue.VELOCITY_VOLTAGE_FOC.value: self._get_differential_pid_motor_voltage_feed_forward(),
            DifferentialControlModeValue.MOTION_MAGIC_VOLTAGE.value: self._get_differential_pid_motor_voltage_feed_forward(),
            DifferentialControlModeValue.MOTION_MAGIC_VOLTAGE_FOC.value: self._get_differential_pid_motor_voltage_feed_forward(),
            DifferentialControlModeValue.POSITION_TORQUE_CURRENT_FOC.value: self._get_differential_pid_torque_current_feed_forward(),
            DifferentialControlModeValue.VELOCITY_TORQUE_CURRENT_FOC.value: self._get_differential_pid_torque_current_feed_forward(),
            DifferentialControlModeValue.MOTION_MAGIC_TORQUE_CURRENT_FOC.value: self._get_differential_pid_torque_current_feed_forward(),
        }
        return self._common_lookup(SpnValue.TALON_FX_DIFFERENTIAL_CONTROL_MODE.value, 12, map_filler, "differential_closed_loop_feed_forward", True, float)
    
    def get_differential_closed_loop_derivative_output(self) -> StatusSignal[float]:
        """
        Differential closed loop derivative component
        
        The portion of the differential closed loop output that is the
        proportional to the deriviative the error. Alternatively, the
        d-Contribution of the closed loop output.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns:  DifferentialClosedLoopDerivativeOutput Status Signal object
        """
        map_filler = lambda: {
            DifferentialControlModeValue.POSITION_DUTY_CYCLE.value: self._get_differential_pid_duty_cycle_derivative_output(),
            DifferentialControlModeValue.POSITION_DUTY_CYCLE_FOC.value: self._get_differential_pid_duty_cycle_derivative_output(),
            DifferentialControlModeValue.VELOCITY_DUTY_CYCLE.value: self._get_differential_pid_duty_cycle_derivative_output(),
            DifferentialControlModeValue.VELOCITY_DUTY_CYCLE_FOC.value: self._get_differential_pid_duty_cycle_derivative_output(),
            DifferentialControlModeValue.MOTION_MAGIC_DUTY_CYCLE.value: self._get_differential_pid_duty_cycle_derivative_output(),
            DifferentialControlModeValue.MOTION_MAGIC_DUTY_CYCLE_FOC.value: self._get_differential_pid_duty_cycle_derivative_output(),
            DifferentialControlModeValue.POSITION_VOLTAGE.value: self._get_diff_pid_motor_voltage_derivative_output(),
            DifferentialControlModeValue.POSITION_VOLTAGE_FOC.value: self._get_diff_pid_motor_voltage_derivative_output(),
            DifferentialControlModeValue.VELOCITY_VOLTAGE.value: self._get_diff_pid_motor_voltage_derivative_output(),
            DifferentialControlModeValue.VELOCITY_VOLTAGE_FOC.value: self._get_diff_pid_motor_voltage_derivative_output(),
            DifferentialControlModeValue.MOTION_MAGIC_VOLTAGE.value: self._get_diff_pid_motor_voltage_derivative_output(),
            DifferentialControlModeValue.MOTION_MAGIC_VOLTAGE_FOC.value: self._get_diff_pid_motor_voltage_derivative_output(),
            DifferentialControlModeValue.POSITION_TORQUE_CURRENT_FOC.value: self._get_differential_pid_torque_current_derivative_output(),
            DifferentialControlModeValue.VELOCITY_TORQUE_CURRENT_FOC.value: self._get_differential_pid_torque_current_derivative_output(),
            DifferentialControlModeValue.MOTION_MAGIC_TORQUE_CURRENT_FOC.value: self._get_differential_pid_torque_current_derivative_output(),
        }
        return self._common_lookup(SpnValue.TALON_FX_DIFFERENTIAL_CONTROL_MODE.value, 13, map_filler, "differential_closed_loop_derivative_output", True, float)
    
    def get_differential_closed_loop_output(self) -> StatusSignal[float]:
        """
        Differential closed loop total output
        
        The total output of the differential closed loop output.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns:  DifferentialClosedLoopOutput Status Signal object
        """
        map_filler = lambda: {
            DifferentialControlModeValue.POSITION_DUTY_CYCLE.value: self._get_differential_pid_duty_cycle_output(),
            DifferentialControlModeValue.POSITION_DUTY_CYCLE_FOC.value: self._get_differential_pid_duty_cycle_output(),
            DifferentialControlModeValue.VELOCITY_DUTY_CYCLE.value: self._get_differential_pid_duty_cycle_output(),
            DifferentialControlModeValue.VELOCITY_DUTY_CYCLE_FOC.value: self._get_differential_pid_duty_cycle_output(),
            DifferentialControlModeValue.MOTION_MAGIC_DUTY_CYCLE.value: self._get_differential_pid_duty_cycle_output(),
            DifferentialControlModeValue.MOTION_MAGIC_DUTY_CYCLE_FOC.value: self._get_differential_pid_duty_cycle_output(),
            DifferentialControlModeValue.POSITION_VOLTAGE.value: self._get_differential_pid_motor_voltage_output(),
            DifferentialControlModeValue.POSITION_VOLTAGE_FOC.value: self._get_differential_pid_motor_voltage_output(),
            DifferentialControlModeValue.VELOCITY_VOLTAGE.value: self._get_differential_pid_motor_voltage_output(),
            DifferentialControlModeValue.VELOCITY_VOLTAGE_FOC.value: self._get_differential_pid_motor_voltage_output(),
            DifferentialControlModeValue.MOTION_MAGIC_VOLTAGE.value: self._get_differential_pid_motor_voltage_output(),
            DifferentialControlModeValue.MOTION_MAGIC_VOLTAGE_FOC.value: self._get_differential_pid_motor_voltage_output(),
            DifferentialControlModeValue.POSITION_TORQUE_CURRENT_FOC.value: self._get_differential_pid_torque_current_output(),
            DifferentialControlModeValue.VELOCITY_TORQUE_CURRENT_FOC.value: self._get_differential_pid_torque_current_output(),
            DifferentialControlModeValue.MOTION_MAGIC_TORQUE_CURRENT_FOC.value: self._get_differential_pid_torque_current_output(),
        }
        return self._common_lookup(SpnValue.TALON_FX_DIFFERENTIAL_CONTROL_MODE.value, 14, map_filler, "differential_closed_loop_output", True, float)
    
    def get_differential_closed_loop_reference(self) -> StatusSignal[float]:
        """
        Value that the differential closed loop is targeting
        
        This is the value that the differential closed loop PID controller
        targets.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns:  DifferentialClosedLoopReference Status Signal object
        """
        map_filler = lambda: {
            DifferentialControlModeValue.POSITION_DUTY_CYCLE.value: self._get_differential_pid_position_reference(),
            DifferentialControlModeValue.POSITION_DUTY_CYCLE_FOC.value: self._get_differential_pid_position_reference(),
            DifferentialControlModeValue.MOTION_MAGIC_DUTY_CYCLE.value: self._get_differential_pid_position_reference(),
            DifferentialControlModeValue.MOTION_MAGIC_DUTY_CYCLE_FOC.value: self._get_differential_pid_position_reference(),
            DifferentialControlModeValue.POSITION_VOLTAGE.value: self._get_differential_pid_position_reference(),
            DifferentialControlModeValue.POSITION_VOLTAGE_FOC.value: self._get_differential_pid_position_reference(),
            DifferentialControlModeValue.MOTION_MAGIC_VOLTAGE.value: self._get_differential_pid_position_reference(),
            DifferentialControlModeValue.MOTION_MAGIC_VOLTAGE_FOC.value: self._get_differential_pid_position_reference(),
            DifferentialControlModeValue.POSITION_TORQUE_CURRENT_FOC.value: self._get_differential_pid_position_reference(),
            DifferentialControlModeValue.MOTION_MAGIC_TORQUE_CURRENT_FOC.value: self._get_differential_pid_position_reference(),
            DifferentialControlModeValue.VELOCITY_DUTY_CYCLE.value: self._get_differential_pid_velocity_reference(),
            DifferentialControlModeValue.VELOCITY_DUTY_CYCLE_FOC.value: self._get_differential_pid_velocity_reference(),
            DifferentialControlModeValue.VELOCITY_VOLTAGE.value: self._get_differential_pid_velocity_reference(),
            DifferentialControlModeValue.VELOCITY_VOLTAGE_FOC.value: self._get_differential_pid_velocity_reference(),
            DifferentialControlModeValue.VELOCITY_TORQUE_CURRENT_FOC.value: self._get_differential_pid_velocity_reference(),
        }
        return self._common_lookup(SpnValue.TALON_FX_DIFFERENTIAL_CONTROL_MODE.value, 15, map_filler, "differential_closed_loop_reference", True, float)
    
    def get_differential_closed_loop_reference_slope(self) -> StatusSignal[float]:
        """
        Derivative of the target that the differential closed loop is
        targeting
        
        This is the change in the closed loop reference. This may be used in
        the feed-forward calculation, the derivative-error, or in application
        of the signage for kS. Typically, this represents the target velocity
        during Motion Magic®.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns:  DifferentialClosedLoopReferenceSlope Status Signal object
        """
        map_filler = lambda: {
            DifferentialControlModeValue.POSITION_DUTY_CYCLE.value: self._get_differential_pid_position_reference_slope(),
            DifferentialControlModeValue.POSITION_DUTY_CYCLE_FOC.value: self._get_differential_pid_position_reference_slope(),
            DifferentialControlModeValue.MOTION_MAGIC_DUTY_CYCLE.value: self._get_differential_pid_position_reference_slope(),
            DifferentialControlModeValue.MOTION_MAGIC_DUTY_CYCLE_FOC.value: self._get_differential_pid_position_reference_slope(),
            DifferentialControlModeValue.POSITION_VOLTAGE.value: self._get_differential_pid_position_reference_slope(),
            DifferentialControlModeValue.POSITION_VOLTAGE_FOC.value: self._get_differential_pid_position_reference_slope(),
            DifferentialControlModeValue.MOTION_MAGIC_VOLTAGE.value: self._get_differential_pid_position_reference_slope(),
            DifferentialControlModeValue.MOTION_MAGIC_VOLTAGE_FOC.value: self._get_differential_pid_position_reference_slope(),
            DifferentialControlModeValue.POSITION_TORQUE_CURRENT_FOC.value: self._get_differential_pid_position_reference_slope(),
            DifferentialControlModeValue.MOTION_MAGIC_TORQUE_CURRENT_FOC.value: self._get_differential_pid_position_reference_slope(),
            DifferentialControlModeValue.VELOCITY_DUTY_CYCLE.value: self._get_differential_pid_velocity_reference_slope(),
            DifferentialControlModeValue.VELOCITY_DUTY_CYCLE_FOC.value: self._get_differential_pid_velocity_reference_slope(),
            DifferentialControlModeValue.VELOCITY_VOLTAGE.value: self._get_differential_pid_velocity_reference_slope(),
            DifferentialControlModeValue.VELOCITY_VOLTAGE_FOC.value: self._get_differential_pid_velocity_reference_slope(),
            DifferentialControlModeValue.VELOCITY_TORQUE_CURRENT_FOC.value: self._get_differential_pid_velocity_reference_slope(),
        }
        return self._common_lookup(SpnValue.TALON_FX_DIFFERENTIAL_CONTROL_MODE.value, 16, map_filler, "differential_closed_loop_reference_slope", True, float)
    
    def get_differential_closed_loop_error(self) -> StatusSignal[float]:
        """
        The difference between target differential reference and current
        measurement
        
        This is the value that is treated as the error in the differential PID
        loop.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :returns:  DifferentialClosedLoopError Status Signal object
        """
        map_filler = lambda: {
            DifferentialControlModeValue.POSITION_DUTY_CYCLE.value: self._get_differential_pid_position_closed_loop_error(),
            DifferentialControlModeValue.POSITION_DUTY_CYCLE_FOC.value: self._get_differential_pid_position_closed_loop_error(),
            DifferentialControlModeValue.MOTION_MAGIC_DUTY_CYCLE.value: self._get_differential_pid_position_closed_loop_error(),
            DifferentialControlModeValue.MOTION_MAGIC_DUTY_CYCLE_FOC.value: self._get_differential_pid_position_closed_loop_error(),
            DifferentialControlModeValue.POSITION_VOLTAGE.value: self._get_differential_pid_position_closed_loop_error(),
            DifferentialControlModeValue.POSITION_VOLTAGE_FOC.value: self._get_differential_pid_position_closed_loop_error(),
            DifferentialControlModeValue.MOTION_MAGIC_VOLTAGE.value: self._get_differential_pid_position_closed_loop_error(),
            DifferentialControlModeValue.MOTION_MAGIC_VOLTAGE_FOC.value: self._get_differential_pid_position_closed_loop_error(),
            DifferentialControlModeValue.POSITION_TORQUE_CURRENT_FOC.value: self._get_differential_pid_position_closed_loop_error(),
            DifferentialControlModeValue.MOTION_MAGIC_TORQUE_CURRENT_FOC.value: self._get_differential_pid_position_closed_loop_error(),
            DifferentialControlModeValue.VELOCITY_DUTY_CYCLE.value: self._get_differential_pid_velocity_closed_loop_error(),
            DifferentialControlModeValue.VELOCITY_DUTY_CYCLE_FOC.value: self._get_differential_pid_velocity_closed_loop_error(),
            DifferentialControlModeValue.VELOCITY_VOLTAGE.value: self._get_differential_pid_velocity_closed_loop_error(),
            DifferentialControlModeValue.VELOCITY_VOLTAGE_FOC.value: self._get_differential_pid_velocity_closed_loop_error(),
            DifferentialControlModeValue.VELOCITY_TORQUE_CURRENT_FOC.value: self._get_differential_pid_velocity_closed_loop_error(),
        }
        return self._common_lookup(SpnValue.TALON_FX_DIFFERENTIAL_CONTROL_MODE.value, 17, map_filler, "differential_closed_loop_error", True, float)
    

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
        if isinstance(request, (DutyCycleOut, TorqueCurrentFOC, VoltageOut, PositionDutyCycle, PositionVoltage, PositionTorqueCurrentFOC, VelocityDutyCycle, VelocityVoltage, VelocityTorqueCurrentFOC, MotionMagicDutyCycle, MotionMagicVoltage, MotionMagicTorqueCurrentFOC, DifferentialDutyCycle, DifferentialVoltage, DifferentialPositionDutyCycle, DifferentialPositionVoltage, DifferentialVelocityDutyCycle, DifferentialVelocityVoltage, DifferentialMotionMagicDutyCycle, DifferentialMotionMagicVoltage, Follower, StrictFollower, DifferentialFollower, DifferentialStrictFollower, NeutralOut, CoastOut, StaticBrake, MusicTone, MotionMagicVelocityDutyCycle, MotionMagicVelocityTorqueCurrentFOC, MotionMagicVelocityVoltage, MotionMagicExpoDutyCycle, MotionMagicExpoVoltage, MotionMagicExpoTorqueCurrentFOC, DynamicMotionMagicDutyCycle, DynamicMotionMagicVoltage, DynamicMotionMagicTorqueCurrentFOC)):
            return self._set_control_private(request)
        return StatusCode.NOT_SUPPORTED

    
    def set_position(self, new_value: rotation, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Sets the mechanism position of the device in mechanism rotations.
        
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
    
    def clear_sticky_fault_proc_temp(self, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Clear sticky fault: Processor temperature exceeded limit
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_proc_temp(timeout_seconds)
    
    def clear_sticky_fault_device_temp(self, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Clear sticky fault: Device temperature exceeded limit
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_device_temp(timeout_seconds)
    
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
    
    def clear_sticky_fault_bridge_brownout(self, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Clear sticky fault: Bridge was disabled most likely due to supply
        voltage dropping too low.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_bridge_brownout(timeout_seconds)
    
    def clear_sticky_fault_remote_sensor_reset(self, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Clear sticky fault: The remote sensor has reset.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_remote_sensor_reset(timeout_seconds)
    
    def clear_sticky_fault_missing_differential_fx(self, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Clear sticky fault: The remote Talon FX used for differential control
        is not present on CAN Bus.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_missing_differential_fx(timeout_seconds)
    
    def clear_sticky_fault_remote_sensor_pos_overflow(self, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Clear sticky fault: The remote sensor position has overflowed. Because
        of the nature of remote sensors, it is possible for the remote sensor
        position to overflow beyond what is supported by the status signal
        frame. However, this is rare and cannot occur over the course of an
        FRC match under normal use.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_remote_sensor_pos_overflow(timeout_seconds)
    
    def clear_sticky_fault_over_supply_v(self, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Clear sticky fault: Supply Voltage has exceeded the maximum voltage
        rating of device.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_over_supply_v(timeout_seconds)
    
    def clear_sticky_fault_unstable_supply_v(self, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Clear sticky fault: Supply Voltage is unstable.  Ensure you are using
        a battery and current limited power supply.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_unstable_supply_v(timeout_seconds)
    
    def clear_sticky_fault_reverse_hard_limit(self, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Clear sticky fault: Reverse limit switch has been asserted.  Output is
        set to neutral.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_reverse_hard_limit(timeout_seconds)
    
    def clear_sticky_fault_forward_hard_limit(self, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Clear sticky fault: Forward limit switch has been asserted.  Output is
        set to neutral.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_forward_hard_limit(timeout_seconds)
    
    def clear_sticky_fault_reverse_soft_limit(self, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Clear sticky fault: Reverse soft limit has been asserted.  Output is
        set to neutral.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_reverse_soft_limit(timeout_seconds)
    
    def clear_sticky_fault_forward_soft_limit(self, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Clear sticky fault: Forward soft limit has been asserted.  Output is
        set to neutral.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_forward_soft_limit(timeout_seconds)
    
    def clear_sticky_fault_remote_sensor_data_invalid(self, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Clear sticky fault: The remote sensor's data is no longer trusted.
        This can happen if the remote sensor disappears from the CAN bus or if
        the remote sensor indicates its data is no longer valid, such as when
        a CANcoder's magnet strength falls into the "red" range.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_remote_sensor_data_invalid(timeout_seconds)
    
    def clear_sticky_fault_fused_sensor_out_of_sync(self, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Clear sticky fault: The remote sensor used for fusion has fallen out
        of sync to the local sensor. A re-synchronization has occurred, which
        may cause a discontinuity. This typically happens if there is
        significant slop in the mechanism, or if the RotorToSensorRatio
        configuration parameter is incorrect.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_fused_sensor_out_of_sync(timeout_seconds)
    
    def clear_sticky_fault_stator_curr_limit(self, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Clear sticky fault: Stator current limit occured.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_stator_curr_limit(timeout_seconds)
    
    def clear_sticky_fault_supply_curr_limit(self, timeout_seconds: second = 0.050) -> StatusCode:
        """
        Clear sticky fault: Supply current limit occured.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_supply_curr_limit(timeout_seconds)

