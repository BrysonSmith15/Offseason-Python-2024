"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

import ctypes as c
import os, pkg_resources

class ReturnValues(c.Structure):
    _fields_ = [
        ("outValue", c.c_double),
        ("units", c.c_char_p),
        ("hwtimestampseconds", c.c_double),
        ("swtimestampseconds", c.c_double),
        ("ecutimestampseconds", c.c_double),
        ("error", c.c_int),
    ]

class SignalValues(c.Structure):
    _fields_ = [
        ("devicehash", c.c_uint32),
        ("spn", c.c_uint32),
    ]

class NetworkSignals(c.Structure):
    _fields_ = [
        ("network", c.c_char_p),
        ("signal", SignalValues),
    ]

class Native:
    """
    Class to use for referencing c functions in the
    Phoenix6 C API
    """

    __instance = None

    __c_args = [
        ("c_ctre_phoenix6_get_current_time_seconds", c.c_double, []),
        ("c_ctre_phoenix6_is_simulation", c.c_bool, []),
        (
            "c_ctre_phoenix6_get_rets",
            c.c_int,
            [c.c_uint16, c.c_int, c.POINTER(ReturnValues)],
        ),
        (
            "c_ctre_phoenix6_encode_device",
            c.c_int,
            [c.c_int, c.c_char_p, c.c_char_p, c.POINTER(c.c_uint32)],
        ),
        (
            "c_ctre_phoenix6_get_signal",
            c.c_int,
            [c.c_size_t, c.POINTER(SignalValues), c.POINTER(ReturnValues), c.c_char_p, c.c_bool, c.c_double]
        ),
        (
            "c_ctre_phoenix6_SetUpdateFrequency",
            c.c_int,
            [c.c_int, c.c_char_p, c.c_uint32, c.c_uint16, c.c_double, c.c_double]
        ),
        (
            "c_ctre_phoenix6_SetUpdateFrequencyForAll",
            c.c_int,
            [c.c_int, c.POINTER(NetworkSignals), c.c_size_t, c.c_double, c.c_double]
        ),
        (
            "c_ctre_phoenix6_GetUpdateFrequency",
            c.c_double,
            [c.c_char_p, c.c_uint32, c.c_uint16]
        ),
        (
            "c_ctre_phoenix6_OptimizeUpdateFrequencies",
            c.c_int,
            [c.c_int, c.c_char_p, c.c_uint32, c.c_double, c.c_double]
        ),
        (
            "c_ctre_phoenix6_unmanaged_feed_enable",
            c.c_int,
            [c.c_int32]
        ),
        (
            "c_ctre_phoenix6_unmanaged_get_api_compliancy",
            c.c_int,
            []
        ),
        (
            "c_ctre_phoenix_report_error",
            None,
            [c.c_int, c.c_int32, c.c_int, c.c_char_p, c.c_char_p, c.c_char_p]
        ),
        (
            "c_ctre_phoenix6_set_configs",
            c.c_int,
            [c.c_int, c.c_char_p, c.c_int, c.c_double, c.c_char_p, c.c_uint32, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_get_configs",
            c.c_int,
            [c.c_int, c.c_char_p, c.c_int, c.c_double, c.POINTER(c.c_char_p), c.c_bool]
        ),
        (
            "c_ctre_phoenix6_serialize_double",
            c.c_int,
            [c.c_int, c.c_double, c.POINTER(c.c_char_p)]
        ),
        (
            "c_ctre_phoenix6_serialize_int",
            c.c_int,
            [c.c_int, c.c_int, c.POINTER(c.c_char_p)]
        ),
        (
            "c_ctre_phoenix6_serialize_bool",
            c.c_int,
            [c.c_int, c.c_bool, c.POINTER(c.c_char_p)]
        ),
        (
            "c_ctre_phoenix6_serialize_pgn",
            c.c_int,
            [c.c_int, c.c_uint16, c.c_uint16, c.POINTER(c.c_char_p)]
        ),
        (
            "c_ctre_phoenix6_deserialize_double",
            c.c_int,
            [c.c_int, c.c_char_p, c.c_uint32, c.POINTER(c.c_double)]
        ),
        (
            "c_ctre_phoenix6_deserialize_int",
            c.c_int,
            [c.c_int, c.c_char_p, c.c_uint32, c.POINTER(c.c_int)]
        ),
        (
            "c_ctre_phoenix6_deserialize_bool",
            c.c_int,
            [c.c_int, c.c_char_p, c.c_uint32, c.POINTER(c.c_bool)]
        ),
        (
            "c_ctre_phoenix6_deserialize_pgn",
            c.c_int,
            [c.c_int, c.c_char_p, c.c_uint32, c.POINTER(c.c_uint16), c.POINTER(c.c_uint16)]
        ),
        (
            "c_ctre_phoenix6_free_memory",
            c.c_int,
            [c.POINTER(c.c_char_p)]
        ),
        (
            "c_ctre_phoenix6_platform_canbus_is_network_fd",
            c.c_bool,
            [c.c_char_p]
        ),
        (
            "c_ctre_phoenix6_platform_canbus_get_status",
            c.c_int32,
            [c.POINTER(c.c_float), c.POINTER(c.c_uint32), c.POINTER(c.c_uint32), c.POINTER(c.c_uint32), c.POINTER(c.c_uint32), c.c_char_p, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_platform_sim_create",
            c.c_int32,
            [c.c_int, c.c_int]
        ),
        (
            "c_ctre_phoenix6_platform_sim_destroy",
            c.c_int32,
            [c.c_int, c.c_int]
        ),
        (
            "c_ctre_phoenix6_platform_sim_destroy_all",
            c.c_int32,
            []
        ),
        (
            "c_ctre_phoenix6_platform_sim_set_physics_input",
            c.c_int32,
            [c.c_int, c.c_int, c.c_char_p, c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_sim_get_physics_value",
            c.c_int32,
            [c.c_int, c.c_int, c.c_char_p, c.POINTER(c.c_double)]
        ),
        (
            "c_ctre_phoenix6_platform_sim_get_last_error",
            c.c_int32,
            [c.c_int, c.c_int]
        ),
        (
            "c_ctre_phoenix6_platform_set_logger_path",
            c.c_int32,
            [c.c_char_p]
        ),
        (
            "c_ctre_phoenix6_platform_start_logger",
            c.c_int32,
            []
        ),
        (
            "c_ctre_phoenix6_platform_stop_logger",
            c.c_int32,
            []
        ),
        (
            "c_ctre_phoenix6_platform_enable_auto_logging",
            c.c_int32,
            [c.c_bool]
        ),
        (
            "c_ctre_phoenix6_platform_write_raw",
            c.c_int32,
            [c.c_char_p, c.POINTER(c.c_uint8), c.c_uint8, c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_write_boolean",
            c.c_int32,
            [c.c_char_p, c.c_bool, c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_write_integer",
            c.c_int32,
            [c.c_char_p, c.c_int64, c.c_char_p, c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_write_float",
            c.c_int32,
            [c.c_char_p, c.c_float, c.c_char_p, c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_write_double",
            c.c_int32,
            [c.c_char_p, c.c_double, c.c_char_p, c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_write_string",
            c.c_int32,
            [c.c_char_p, c.c_char_p, c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_write_boolean_array",
            c.c_int32,
            [c.c_char_p, c.POINTER(c.c_bool), c.c_uint8, c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_write_integer_array",
            c.c_int32,
            [c.c_char_p, c.POINTER(c.c_int64), c.c_uint8, c.c_char_p, c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_write_float_array",
            c.c_int32,
            [c.c_char_p, c.POINTER(c.c_float), c.c_uint8, c.c_char_p, c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_write_double_array",
            c.c_int32,
            [c.c_char_p, c.POINTER(c.c_double), c.c_uint8, c.c_char_p, c.c_double]
        ),
        (
            "c_ctre_phoenix6_orchestra_Create",
            c.c_int,
            [c.POINTER(c.c_uint16)]
        ),
        (
            "c_ctre_phoenix6_orchestra_Close",
            c.c_int,
            [c.c_uint16]
        ),
        (
            "c_ctre_phoenix6_orchestra_AddDevice",
            c.c_int,
            [c.c_uint16, c.c_char_p, c.c_uint32]
        ),
        (
            "c_ctre_phoenix6_orchestra_AddDeviceWithTrack",
            c.c_int,
            [c.c_uint16, c.c_char_p, c.c_uint32, c.c_uint16]
        ),
        (
            "c_ctre_phoenix6_orchestra_ClearDevices",
            c.c_int,
            [c.c_uint16]
        ),
        (
            "c_ctre_phoenix6_orchestra_LoadMusic",
            c.c_int,
            [c.c_uint16, c.c_char_p]
        ),
        (
            "c_ctre_phoenix6_orchestra_Play",
            c.c_int,
            [c.c_uint16]
        ),
        (
            "c_ctre_phoenix6_orchestra_Pause",
            c.c_int,
            [c.c_uint16]
        ),
        (
            "c_ctre_phoenix6_orchestra_Stop",
            c.c_int,
            [c.c_uint16]
        ),
        (
            "c_ctre_phoenix6_orchestra_IsPlaying",
            c.c_int,
            [c.c_uint16, c.POINTER(c.c_int)]
        ),
        (
            "c_ctre_phoenix6_orchestra_GetCurrentTime",
            c.c_int,
            [c.c_uint16, c.POINTER(c.c_double)]
        ),
        (
            "c_ctre_phoenix6_RequestControlDutyCycleOut",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlTorqueCurrentFOC",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlVoltageOut",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlPositionDutyCycle",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlPositionVoltage",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlPositionTorqueCurrentFOC",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlVelocityDutyCycle",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlVelocityVoltage",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlVelocityTorqueCurrentFOC",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlMotionMagicDutyCycle",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlMotionMagicVoltage",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlMotionMagicTorqueCurrentFOC",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDifferentialDutyCycle",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDifferentialVoltage",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDifferentialPositionDutyCycle",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_int, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDifferentialPositionVoltage",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_int, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDifferentialVelocityDutyCycle",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_int, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDifferentialVelocityVoltage",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_int, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDifferentialMotionMagicDutyCycle",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_int, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDifferentialMotionMagicVoltage",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_int, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlFollower",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_int, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlStrictFollower",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_int]
        ),
        (
            "c_ctre_phoenix6_RequestControlDifferentialFollower",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_int, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDifferentialStrictFollower",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_int]
        ),
        (
            "c_ctre_phoenix6_RequestControlNeutralOut",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlCoastOut",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlStaticBrake",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlBalanceBattery",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlBMSManualIsolator",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlBMSManualVboost",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_bool, c.c_double, c.c_double]
        ),
        (
            "c_ctre_phoenix6_RequestControlBMSManualPwmJunction",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_int, c.c_double]
        ),
        (
            "c_ctre_phoenix6_RequestControlBMSClearFault",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlMusicTone",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double]
        ),
        (
            "c_ctre_phoenix6_RequestControlMotionMagicVelocityDutyCycle",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlMotionMagicVelocityTorqueCurrentFOC",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlMotionMagicVelocityVoltage",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlMotionMagicExpoDutyCycle",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlMotionMagicExpoVoltage",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlMotionMagicExpoTorqueCurrentFOC",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDynamicMotionMagicDutyCycle",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDynamicMotionMagicVoltage",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDynamicMotionMagicTorqueCurrentFOC",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool, c.c_double, c.c_double, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool]
        ),
    ]
    """
    Function prototypes for C methods.

    Format is tuple[str, ctype, list[ctype]]

    First Parameter str is name of function
    Second Parameter ctype is return of function
    Third Parameter list[ctype] are the arguments of the function
    """

    @classmethod
    def instance(clazz):
        """
        Get instance of the native class to
        reference c API calls.
        """
        if clazz.__instance is None:
            hardware_libs = ["CTRE_PhoenixTools"]
            sim_libs = [
                "CTRE_SimCANCoder",
                "CTRE_SimPigeonIMU",
                "CTRE_SimProCANcoder",
                "CTRE_SimProPigeon2",
                "CTRE_SimProTalonFX",
                "CTRE_SimTalonFX",
                "CTRE_SimTalonSRX",
                "CTRE_SimVictorSPX",
                "CTRE_PhoenixTools_Sim" # Make sure Tools_Sim is loaded last
            ]

            library_path = pkg_resources.resource_filename("phoenix6", "lib/")
            if os.name == "nt": # Windows will return nt
                extension = ".dll"
                prefix = ""
            elif os.uname().sysname == "Linux": # Perform uname to delineate between mac and linux
                extension = ".so"
                prefix = "lib"
            else:
                extension = ".dylib"
                prefix = "lib"

            # If we're explicitly targeting hardware, use hardware. Otherwise use software
            if "CTR_TARGET" in os.environ and os.environ["CTR_TARGET"] == "Hardware":
                first_load = hardware_libs
                second_load = sim_libs
            else:
                first_load = sim_libs
                second_load = hardware_libs

            try:
                # First try our desired target
                for lib in first_load:
                    clazz.__instance = c.cdll.LoadLibrary(library_path + prefix + lib + extension)
            except:
                try:
                    # If we fail, then load the second target
                    for lib in second_load:
                        clazz.__instance = c.cdll.LoadLibrary(library_path + prefix + lib + extension)
                except:
                    raise FileNotFoundError("Could not find an appropriate CTRE library to load")

            # And move on to declaring all the C functions we need access to
            for method, rtype, argtypes in clazz.__c_args:
                c_func = clazz.__instance.__getattr__(method)
                c_func.restype = rtype
                c_func.argtypes = argtypes
        return clazz.__instance
