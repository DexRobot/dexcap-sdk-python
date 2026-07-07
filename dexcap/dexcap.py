import ctypes
import sys
from ctypes import *
from enum import IntEnum

if sys.platform.startswith('win'):
    LibDexCapSuit = cdll.LoadLibrary("../contrib/dexcap-sdk-cpp/libs/windows/DexCap.dll")
else:
    LibDexCapSuit = cdll.LoadLibrary("../contrib/dexcap-sdk-cpp/libs/linux/libDexCap.so")


class AdapterType(IntEnum):
    """Supported connection adapters"""
    INVALID = 0
    WIREDUSB = 0x01
    WIRELESS = 0x02
    COMMONUSB = 0x03
    BLUETOOTH = 0x04
    MODBUSUSB = 0x06


class DexCapDeviceType(IntEnum):
    UnDefn = 0x00
    LGlove = 0x01
    RGlove = 0x02
    UpBody = 0x04
    IMUnit = 0x08
    WRecvr = 0x20


class DexReturn(IntEnum):
    DEX_ERROR = -1,
    DEX_INVALID_DEVICE = -2,
    DEX_INVALID_INSTANCE = -3,
    DEX_INVALID_DATA_FMT = -4,
    DEX_DEV_TYPE_MISMATCH = -5,

    DEX_SUCCESS = 0,
    DEX_SUCCESS_WITH_INFO = 1,
    DEX_REQUEST_TIMEOUT = 2,
    DEX_SEC_ON_WITHOUT_KEY = 3,
    DEX_BLE_CONN_UNSECURED = 4,
    DEX_STRING_TRUNCATED = 6,
    DEX_NO_DATA = 100,


DexCapDeviceData = ctypes.c_uint16 * 24
EndPoseData = ctypes.c_double * 4 * 4
IMUPoseData = ctypes.c_float * 17

DEV_TYPE_PTR = POINTER(DexCapDeviceType)


class GloveJointAngles(ctypes.Structure):
    _fields_ = [
        ("ThumbDIP", ctypes.c_uint16),
        ("ThumbPIP", ctypes.c_uint16),
        ("ThumbMCP", ctypes.c_uint16),
        ("ThumbSWP", ctypes.c_uint16),
        ("ThumbROP", ctypes.c_uint16),
        ("IndexDIP", ctypes.c_uint16),
        ("IndexPIP", ctypes.c_uint16),
        ("IndexMCP", ctypes.c_uint16),
        ("IndexSWP", ctypes.c_uint16),
        ("MiddleDIP", ctypes.c_uint16),
        ("MiddlePIP", ctypes.c_uint16),
        ("MiddleMCP", ctypes.c_uint16),
        ("MiddleSWP", ctypes.c_uint16),
        ("RingDIP", ctypes.c_uint16),
        ("RingPIP", ctypes.c_uint16),
        ("RingMCP", ctypes.c_uint16),
        ("RingSWP", ctypes.c_uint16),
        ("LittleDIP", ctypes.c_uint16),
        ("LittlePIP", ctypes.c_uint16),
        ("LittleMCP", ctypes.c_uint16),
        ("LittleSWP", ctypes.c_uint16),
        ("BatteryState", ctypes.c_uint16),
        ("ErrorMask", ctypes.c_uint32),
        ("timestamp", ctypes.c_uint64),
    ]

class BodyJointAngles(ctypes.Structure):
    _fields_ = [
        ("LArm1", ctypes.c_uint16),
        ("LArm2", ctypes.c_uint16),
        ("LArm3", ctypes.c_uint16),
        ("LArm4", ctypes.c_uint16),
        ("LArm5", ctypes.c_uint16),
        ("LArm6", ctypes.c_uint16),
        ("LArm7", ctypes.c_uint16),
        ("LArm8", ctypes.c_uint16),
        ("LArm9", ctypes.c_uint16),
        ("RArm1", ctypes.c_uint16),
        ("RArm2", ctypes.c_uint16),
        ("RArm3", ctypes.c_uint16),
        ("RArm4", ctypes.c_uint16),
        ("RArm5", ctypes.c_uint16),
        ("RArm6", ctypes.c_uint16),
        ("RArm7", ctypes.c_uint16),
        ("RArm8", ctypes.c_uint16),
        ("RArm9", ctypes.c_uint16),
        ("Back1", ctypes.c_uint16),
        ("Back2", ctypes.c_uint16),
        ("Back3", ctypes.c_uint16),
        ("Back4", ctypes.c_uint16),
        ("Back5", ctypes.c_uint16),
        ("Reserved", ctypes.c_uint16),
        ("timestamp", ctypes.c_uint64),
    ]


class InetMUData(ctypes.Structure):
    _fields_ = [
        ("sys_time", ctypes.c_uint32),
        ("poseData", IMUPoseData),
        ("temperature", ctypes.c_int8),
    ]

class DexCapJointData(ctypes.Structure):
    _fields_ = [
        ("mask", ctypes.c_uint32),
        ("LGlove", DexCapDeviceData),
        ("ExBody", DexCapDeviceData),
        ("RGlove", DexCapDeviceData),
        ("InetMU", InetMUData),
        ("timestamp", ctypes.c_uint64),
    ]


class DexCapEndPoses(ctypes.Structure):
    _fields_ = [
        ("LArm", EndPoseData),
        ("RArm", EndPoseData),
        ("timestamp", ctypes.c_uint64),
    ]


class MainBatteryState(ctypes.Structure):
    _fields_ = [
        ("Currency",     ctypes.c_int16),
        ("Voltage",      ctypes.c_uint16),
        ("RemainPower",  ctypes.c_uint16),
        ("Temperature",  ctypes.c_uint16),
        ("StatusBitmap", ctypes.c_uint16),
        ("Reserved", ctypes.c_uint16),
    ]


class DexCapSuit:
    def __init__(self, adapter_type: AdapterType):
        self.instance = None
        self.available = False
        LibDexCapSuit.dexcap_create_suit_instance.argtypes = [c_void_p]
        LibDexCapSuit.dexcap_create_suit_instance.restype = c_int

        LibDexCapSuit.dexcap_connect_suit_device.argtypes = [c_void_p, c_char_p, DEV_TYPE_PTR, AdapterType]
        LibDexCapSuit.dexcap_connect_suit_device.restype = c_int

        LibDexCapSuit.dexcap_is_device_connected.argtypes = [c_void_p, DexCapDeviceType]
        LibDexCapSuit.dexcap_is_device_connected.restype = c_bool

        LibDexCapSuit.dexcap_disconnect_all_devices.argtypes = [c_void_p]
        LibDexCapSuit.dexcap_disconnect_all_devices.restype = c_int

        LibDexCapSuit.dexcap_disconnect_suit_device.argtypes = [c_void_p, DexCapDeviceType]
        LibDexCapSuit.dexcap_disconnect_suit_device.restype = c_int

        LibDexCapSuit.dexcap_start_suit_sampling.argtypes = [c_void_p]
        LibDexCapSuit.dexcap_start_suit_sampling.restype = c_int

        LibDexCapSuit.dexcap_start_device_sampling.argtypes = [c_void_p, DexCapDeviceType]
        LibDexCapSuit.dexcap_start_device_sampling.restype = c_int

        LibDexCapSuit.dexcap_is_device_sampling.argtypes = [c_void_p, DexCapDeviceType]
        LibDexCapSuit.dexcap_is_device_sampling.restype = c_bool

        LibDexCapSuit.dexcap_stop_suit_sampling.argtypes = [c_void_p]
        LibDexCapSuit.dexcap_stop_suit_sampling.restype = c_int

        LibDexCapSuit.dexcap_stop_device_sampling.argtypes = [c_void_p, DexCapDeviceType]
        LibDexCapSuit.dexcap_stop_device_sampling.restype = c_int

        LibDexCapSuit.dexcap_get_l_glove_data.argtypes = [c_void_p, POINTER(GloveJointAngles)]
        LibDexCapSuit.dexcap_get_l_glove_data.restype = c_int

        LibDexCapSuit.dexcap_get_r_glove_data.argtypes = [c_void_p, POINTER(GloveJointAngles)]
        LibDexCapSuit.dexcap_get_r_glove_data.restype = c_int

        LibDexCapSuit.dexcap_get_ex_body_data.argtypes = [c_void_p, POINTER(BodyJointAngles)]
        LibDexCapSuit.dexcap_get_ex_body_data.restype = c_int

        LibDexCapSuit.dexcap_get_joint_data.argtypes = [c_void_p, POINTER(DexCapJointData)]
        LibDexCapSuit.dexcap_get_joint_data.restype = c_int

        LibDexCapSuit.dexcap_get_arm_end_poses.argtypes = [c_void_p, POINTER(DexCapEndPoses)]
        LibDexCapSuit.dexcap_get_arm_end_poses.restype = c_int

        LibDexCapSuit.dexcap_get_l_battery_state.argtypes = [c_void_p, POINTER(c_uint16)]
        LibDexCapSuit.dexcap_get_l_battery_state.restype = c_int

        LibDexCapSuit.dexcap_get_r_battery_state.argtypes = [c_void_p, POINTER(c_uint16)]
        LibDexCapSuit.dexcap_get_r_battery_state.restype = c_int

        LibDexCapSuit.dexcap_get_main_battery_state.argtypes = [c_void_p, POINTER(MainBatteryState)]
        LibDexCapSuit.dexcap_get_main_battery_state.restype = c_int

        LibDexCapSuit.dexcap_get_diagnostics.argtypes = [c_void_p, POINTER(c_int), c_char_p, c_uint64, POINTER(c_uint64)]
        LibDexCapSuit.dexcap_get_diagnostics.restype = c_int

        LibDexCapSuit.dexcap_get_device_diagnostics.argtypes = [c_void_p, c_ubyte, POINTER(c_int), c_char_p, c_uint64, POINTER(c_uint64)]
        LibDexCapSuit.dexcap_get_device_diagnostics.restype = c_int

        ret_code = LibDexCapSuit.dexcap_create_suit_instance(self.instance)
        self.available = (ret_code is DexReturn.DEX_SUCCESS)

def __del__(self):
    return

def is_available(self):
    return self.available

def connect_device(self, adapter_name, adapter_type):
    DEV_TYPE_PTR()
