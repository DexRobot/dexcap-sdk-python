import ctypes
from ctypes import *
from .typedefs import *


class DexCapDeviceInfo(ctypes.Structure):
    _fields_ = [
        ("device_type", ctypes.c_uint8),
        ("enumer_name", ctypes.c_char * 16),
    ]

DeviceInfo_list = POINTER(DexCapDeviceInfo)

class WiredDeviceEnumerator:
    def __init__(self):
        LibDexCapSuit.alloc_serial_port_device_list.argtypes = []
        LibDexCapSuit.alloc_serial_port_device_list.restype = c_void_p

        LibDexCapSuit.free_serial_port_device_list.argtypes = [c_void_p]
        LibDexCapSuit.free_serial_port_device_list.restype = c_void_p

        LibDexCapSuit.enumerate_serial_port_devices.argtypes = [c_int, c_void_p, POINTER(c_uint64)]
        LibDexCapSuit.enumerate_serial_port_devices.restype = c_void_p

        self.__device_list = list()
        self.__device_info_raw_list = ctypes.cast(LibDexCapSuit.alloc_serial_port_device_list(), DeviceInfo_list)
        self.__device_count = ctypes.c_uint64(0)
        if self.__device_info_raw_list is not None:
            LibDexCapSuit.enumerate_serial_port_devices(0x04, self.__device_info_raw_list, byref(self.__device_count))
            for idx in range(self.__device_count.value):
                dev = self.__device_info_raw_list[idx]
                self.__device_list.append(dev.enumer_name.decode('utf-8'))

    def __del__(self):
        LibDexCapSuit.free_serial_port_device_list(self.__device_info_raw_list)

    def number_of_device_candidates(self) -> int:
        return self.__device_count.value

    def get_device_candidates(self) -> list:
        return self.__device_list

    def if_device_enumerated(self, device_name: str) -> bool:
        for name in self.__device_list:
            if name == device_name:
                return True

        return False
