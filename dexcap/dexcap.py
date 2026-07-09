from ctypes import *
from .typedefs import *


class DexCapSuit:
    def __init__(self, adapter_type: AdapterType):
        self.instance = DEXCAP_SUIT_HANDLE()
        self.available = False
        self.adapter_type = adapter_type

        LibDexCapSuit.dexcap_create_suit_instance.argtypes = [ctypes.POINTER(DEXCAP_SUIT_HANDLE)]
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

        ret_code = LibDexCapSuit.dexcap_create_suit_instance(ctypes.byref(self.instance))
        self.available = (DexReturn(ret_code) is DexReturn.DEX_SUCCESS)

    def __del__(self):
        return

    def is_available(self):
        return self.available

    def get_adapter_type(self):
        return self.adapter_type

    def connect_device(self, adapter_name: str, adapter_type: AdapterType) -> DeviceType:
        device_type  = DeviceType_c(DeviceType.UnDefn.value)
        adapter_type = AdapterType_c(adapter_type.value)
        adapter_name_b = adapter_name.encode('utf-8')
        return_code = DexReturn(LibDexCapSuit.dexcap_connect_suit_device(self.instance,
                                                               ctypes.c_char_p(adapter_name_b),
                                                               ctypes.byref(device_type),
                                                               adapter_type))

        if return_code is DexReturn.DEX_SUCCESS:
            if device_type is not DeviceType.UnDefn and device_type is not DeviceType.WRecvr:
                return DeviceType(device_type.value)

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
        return_code = DexReturn(LibDexCapSuit.dexcap_start_suit_sampling(self.instance))
        return return_code

    def start_device_sampling(self, device: DeviceType) -> DexReturn:
        dev_type = DeviceType_c(device)
        return DexReturn(LibDexCapSuit.dexcap_start_device_sampling(self.instance, dev_type))

    def is_device_sampling(self, device: DeviceType) -> bool:
        dev_type = DeviceType_c(device)
        return LibDexCapSuit.dexcap_is_device_sampling(self.instance, dev_type)

    def stop_sampling(self) -> DexReturn:
        return DexReturn(LibDexCapSuit.dexcap_stop_suit_sampling(self.instance))

    def stop_device_sampling(self, device: DeviceType) -> DexReturn:
        dev_type = DeviceType_c(device)
        return DexReturn(LibDexCapSuit.dexcap_stop_device_sampling(self.instance, dev_type))

    def get_l_glove_data(self) -> (bool, GloveJointAngles):
        data = GloveJointAngles()
        data_ptr = GLV_DATA_PTR(data)
        return_code = DexReturn(LibDexCapSuit.dexcap_get_l_glove_data(self.instance, data_ptr))
        if return_code is DexReturn.DEX_SUCCESS:
            return True, data

        return False, data

    def get_r_glove_data(self) -> (bool, GloveJointAngles):
        data = GloveJointAngles()
        data_ptr = GLV_DATA_PTR(data)
        return_code = DexReturn(LibDexCapSuit.dexcap_get_r_glove_data(self.instance, data_ptr))
        if return_code is DexReturn.DEX_SUCCESS:
            return True, data

        return False, data

    def get_ex_body_data(self) -> (bool, BodyJointAngles):
        data = BodyJointAngles()
        data_ptr = BDY_DATA_PTR(data)
        return_code = DexReturn(LibDexCapSuit.dexcap_get_ex_body_data(self.instance, data_ptr))
        if return_code is DexReturn.DEX_SUCCESS:
            return True, data

        return False, data

    def get_suit_joint_data(self) -> (bool, DexCapJointData):
        data = DexCapJointData()
        data_ptr = DEX_DATA_PTR(data)
        return_code = DexReturn(LibDexCapSuit.dexcap_get_joint_data(self.instance, data_ptr))
        if return_code is DexReturn.DEX_SUCCESS:
            return True, data

        return False, data

    def get_arms_end_poses(self) -> (bool, DexCapEndPoses):
        data = DexCapEndPoses()
        data_ptr = POS_DATA_PTR(data)
        return_code = DexReturn(LibDexCapSuit.dexcap_get_arm_end_poses(self.instance, data_ptr))
        if return_code is DexReturn.DEX_SUCCESS:
            return True, data

        return False, data

    def get_l_battery_state(self) -> int:
        level = ctypes.c_uint16(0)
        return_code = DexReturn(LibDexCapSuit.dexcap_get_l_battery_state(self.instance, byref(level)))
        if return_code is DexReturn.DEX_SUCCESS:
            return int(level)

        return -1

    def get_r_battery_state(self) -> int:
        level = ctypes.c_uint16(0)
        return_code = DexReturn(LibDexCapSuit.dexcap_get_r_battery_state(self.instance, byref(level)))
        if return_code is DexReturn.DEX_SUCCESS:
            return int(level)

        return -1

    def get_main_battery_state(self) -> (bool, MainBatteryState):
        data = MainBatteryState()
        data_ptr = BAT_DATA_PTR(data)
        return_code = DexReturn(LibDexCapSuit.dexcap_get_main_battery_state(self.instance, data_ptr))
        if return_code is DexReturn.DEX_SUCCESS:
            return True, data

        return False, data

    def get_diagnostics(self) -> (int, str):
        err_code = ctypes.c_int(0)
        err_info = str()
        err_info_p = ctypes.c_char_p(err_info.encode('utf-8'))
        err_info_len = ctypes.c_uint64(128)
        LibDexCapSuit.dexcap_get_diagnostics(self.instance,
                                             byref(err_code),
                                             err_info_p,
                                             128,
                                             byref(err_info_len))

        return err_code.value, err_info

    def get_device_diagnostics(self, device: DeviceType) -> (int, str):
        err_code = ctypes.c_int(0)
        err_info = str()
        err_info_p = ctypes.c_char_p(err_info.encode('utf-8'))
        err_info_len = ctypes.c_uint64(128)
        LibDexCapSuit.dexcap_get_device_diagnostics(self.instance,
                                                    device,
                                                    byref(err_code),
                                                    err_info_p,
                                                    128,
                                                    byref(err_info_len))

        return err_code.value, err_info
