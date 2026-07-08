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


class DeviceType(IntEnum):
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

AdapterType_c = ctypes.c_int
DeviceType_c = ctypes.c_int
DeviceType_c_ptr = ctypes.POINTER(DeviceType_c)
GLV_DATA_PTR = ctypes.POINTER(GloveJointAngles)
BDY_DATA_PTR = ctypes.POINTER(BodyJointAngles)
DEX_DATA_PTR = ctypes.POINTER(DexCapJointData)
POS_DATA_PTR = ctypes.POINTER(DexCapEndPoses)
BAT_DATA_PTR = ctypes.POINTER(MainBatteryState)

class DexCapSuit:
    def __init__(self, adapter_type: AdapterType):
        self.instance = None
        self.available = False
        self.adapter_type = adapter_type

        print(type(DeviceType_c), DeviceType_c)

        LibDexCapSuit.dexcap_create_suit_instance.argtypes = [c_void_p]
        LibDexCapSuit.dexcap_create_suit_instance.restype = c_int

        LibDexCapSuit.dexcap_connect_suit_device.argtypes = [c_void_p, c_char_p, DeviceType_c_ptr, AdapterType_c]
        LibDexCapSuit.dexcap_connect_suit_device.restype = c_int

        LibDexCapSuit.dexcap_is_device_connected.argtypes = [c_void_p, DeviceType_c]
        LibDexCapSuit.dexcap_is_device_connected.restype = c_bool

        LibDexCapSuit.dexcap_disconnect_all_devices.argtypes = [c_void_p]
        LibDexCapSuit.dexcap_disconnect_all_devices.restype = c_int

        LibDexCapSuit.dexcap_disconnect_suit_device.argtypes = [c_void_p, DeviceType_c]
        LibDexCapSuit.dexcap_disconnect_suit_device.restype = c_int

        LibDexCapSuit.dexcap_start_suit_sampling.argtypes = [c_void_p]
        LibDexCapSuit.dexcap_start_suit_sampling.restype = c_int

        LibDexCapSuit.dexcap_start_device_sampling.argtypes = [c_void_p, DeviceType_c]
        LibDexCapSuit.dexcap_start_device_sampling.restype = c_int

        LibDexCapSuit.dexcap_is_device_sampling.argtypes = [c_void_p, DeviceType_c]
        LibDexCapSuit.dexcap_is_device_sampling.restype = c_bool

        LibDexCapSuit.dexcap_stop_suit_sampling.argtypes = [c_void_p]
        LibDexCapSuit.dexcap_stop_suit_sampling.restype = c_int

        LibDexCapSuit.dexcap_stop_device_sampling.argtypes = [c_void_p, DeviceType_c]
        LibDexCapSuit.dexcap_stop_device_sampling.restype = c_int

        LibDexCapSuit.dexcap_get_l_glove_data.argtypes = [c_void_p, GLV_DATA_PTR]
        LibDexCapSuit.dexcap_get_l_glove_data.restype = c_int

        LibDexCapSuit.dexcap_get_r_glove_data.argtypes = [c_void_p, GLV_DATA_PTR]
        LibDexCapSuit.dexcap_get_r_glove_data.restype = c_int

        LibDexCapSuit.dexcap_get_ex_body_data.argtypes = [c_void_p, BDY_DATA_PTR]
        LibDexCapSuit.dexcap_get_ex_body_data.restype = c_int

        LibDexCapSuit.dexcap_get_joint_data.argtypes = [c_void_p,DEX_DATA_PTR]
        LibDexCapSuit.dexcap_get_joint_data.restype = c_int

        LibDexCapSuit.dexcap_get_arm_end_poses.argtypes = [c_void_p, POS_DATA_PTR]
        LibDexCapSuit.dexcap_get_arm_end_poses.restype = c_int

        LibDexCapSuit.dexcap_get_l_battery_state.argtypes = [c_void_p, POINTER(c_uint16)]
        LibDexCapSuit.dexcap_get_l_battery_state.restype = c_int

        LibDexCapSuit.dexcap_get_r_battery_state.argtypes = [c_void_p, POINTER(c_uint16)]
        LibDexCapSuit.dexcap_get_r_battery_state.restype = c_int

        LibDexCapSuit.dexcap_get_main_battery_state.argtypes = [c_void_p, BAT_DATA_PTR]
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

    def get_adapter_type(self):
        return self.adapter_type

    def connect_device(self, adapter_name: str, adapter_type: AdapterType) -> DeviceType:
        device_type = DeviceType_c(DeviceType.UnDefn.value)
        adaptr_type = AdapterType_c(adapter_type.value)
        return_code = LibDexCapSuit.dexcap_connect_suit_device(self.instance,
                                                               ctypes.c_char_p(adapter_name.encode('utf-8')),
                                                               ctypes.byref(device_type),
                                                               adaptr_type)

        if return_code is DexReturn.DEX_SUCCESS:
            if device_type is not DeviceType.UnDefn and device_type is not DeviceType.WRecvr:
                return DeviceType(device_type)

        return DeviceType.UnDefn

    def disconnect_device(self, device: DeviceType) -> DexReturn:
        dev_type = DeviceType_c(device)
        return LibDexCapSuit.dexcap_disconnect_suit_device(self.instance, dev_type)

    def disconnect_all(self) -> DexReturn:
        return LibDexCapSuit.dexcap_disconnect_all_devices(self.instance)

    def is_device_connected(self, device: DeviceType) -> bool:
        dev_type = DeviceType_c(device)
        return LibDexCapSuit.dexcap_is_device_connected(self.instance, dev_type)

    def start_sampling(self) -> DexReturn:
        return LibDexCapSuit.dexcap_start_suit_sampling(self.instance)

    def start_device_sampling(self, device: DeviceType) -> DexReturn:
        dev_type = DeviceType_c(device)
        return LibDexCapSuit.dexcap_start_device_sampling(self.instance, dev_type)

    def is_device_sampling(self, device: DeviceType) -> bool:
        dev_type = DeviceType_c(device)
        return LibDexCapSuit.dexcap_is_device_sampling(self.instance, dev_type)

    def stop_sampling(self) -> DexReturn:
        return LibDexCapSuit.dexcap_stop_suit_sampling(self.instance)

    def stop_device_sampling(self, device: DeviceType) -> DexReturn:
        dev_type = DeviceType_c(device)
        return LibDexCapSuit.dexcap_stop_device_sampling(self.instance, dev_type)

    def get_l_glove_data(self) -> (bool, GloveJointAngles):
        data = GloveJointAngles()
        data_ptr = GLV_DATA_PTR(data)
        return_code = LibDexCapSuit.dexcap_get_l_glove_data(self.instance, data_ptr)
        if return_code is DexReturn.DEX_SUCCESS:
            return True, data

        return False, data

    def get_r_glove_data(self) -> (bool, GloveJointAngles):
        data = GloveJointAngles()
        data_ptr = GLV_DATA_PTR(data)
        return_code = LibDexCapSuit.dexcap_get_r_glove_data(self.instance, data_ptr)
        if return_code is DexReturn.DEX_SUCCESS:
            return True, data

        return False, data

    def get_ex_body_data(self) -> (bool, BodyJointAngles):
        data = BodyJointAngles()
        data_ptr = BDY_DATA_PTR(data)
        return_code = LibDexCapSuit.dexcap_get_ex_body_data(self.instance, data_ptr)
        if return_code is DexReturn.DEX_SUCCESS:
            return True, data

        return False, data

    def get_suit_joint_data(self) -> (bool, DexCapJointData):
        data = DexCapJointData()
        data_ptr = DEX_DATA_PTR(data)
        return_code = LibDexCapSuit.dexcap_get_joint_data(self.instance, data_ptr)
        if return_code is DexReturn.DEX_SUCCESS:
            return True, data

        return False, data

    def get_arms_end_poses(self) -> (bool, DexCapEndPoses):
        data = DexCapEndPoses()
        data_ptr = POS_DATA_PTR(data)
        return_code = LibDexCapSuit.dexcap_get_arm_end_poses(self.instance, data_ptr)
        if return_code is DexReturn.DEX_SUCCESS:
            return True, data

        return False, data

    def get_l_battery_state(self) -> int:
        level = ctypes.c_uint16(0)
        level_ptr = ctypes.POINTER(level)
        return_code = LibDexCapSuit.dexcap_get_l_battery_state(self.instance, level_ptr)
        if return_code is DexReturn.DEX_SUCCESS:
            return int(level)

        return -1

    def get_r_battery_state(self) -> int:
        level = ctypes.c_uint16(0)
        level_ptr = ctypes.POINTER(level)
        return_code = LibDexCapSuit.dexcap_get_r_battery_state(self.instance, level_ptr)
        if return_code is DexReturn.DEX_SUCCESS:
            return int(level)

        return -1

    def get_main_battery_state(self) -> (bool, MainBatteryState):
        data = MainBatteryState()
        data_ptr = BAT_DATA_PTR(data)
        return_code = LibDexCapSuit.dexcap_get_main_battery_state(self.instance, data_ptr)
        if return_code is DexReturn.DEX_SUCCESS:
            return True, data

        return False, data

    def get_diagnostics(self) -> (int, str):
        err_code = ctypes.c_int(0)
        err_info = str()
        err_code_p = ctypes.POINTER(err_code)
        err_info_p = ctypes.c_char_p(err_info.encode('utf-8'))
        err_info_len_p = ctypes.POINTER(ctypes.c_uint64(128))
        LibDexCapSuit.dexcap_get_diagnostics(self.instance,
                                             err_code_p,
                                             err_info_p,
                                             128,
                                             err_info_len_p)

        return err_code, err_info
