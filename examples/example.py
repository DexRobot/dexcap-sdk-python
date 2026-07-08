import time
from dexcap import *


def main():
    dexcap_suit = DexCapSuit(AdapterType.WIREDUSB)
    if dexcap_suit.is_available() is not True:
        print('DexCapSuit instance created failed')
        return

    adapter_name = '/dev/ttyACM0'
    device_type = dexcap_suit.connect_device(adapter_name, dexcap_suit.get_adapter_type())
    if device_type is DeviceType.UnDefn:
        print('Device {} is not recognized as a DexCap device, either this device is not working or malfunctioning'.format(adapter_name))
        return

    return_code = dexcap_suit.start_sampling()
    if return_code is not DexReturn.DEX_SUCCESS and return_code is not DexReturn.DEX_SUCCESS_WITH_INFO:
        print('Sampling starts failed')
        return

    timeout = False
    start_ts = time.time()
    while timeout is not True:
        res_joint_angles = dexcap_suit.get_suit_joint_data()
        if res_joint_angles[0] is not True:
            continue

        data = res_joint_angles[1]
        if (data.mask & 0x8000) != 0:
            print('[Left Glove]: jnt1={}, jnt2={}, jnt3={}'.format(data.LGlove[0], data.LGlove[1], data.LGlove[2]))

        if (data.mask & 0x4000) != 0:
            print('[Exo UpBody]: jnt1={}, jnt2={}, jnt3={}'.format(data.ExBody[0], data.ExBody[1], data.ExBody[2]))

        if (data.mask & 0x2000) != 0:
            print('[Left Glove]: jnt1={}, jnt2={}, jnt3={}'.format(data.RGlove[0], data.RGlove[1], data.RGlove[2]))

        print('=============================================')

        duration = time.time() - start_ts
        timeout = duration >= 30

    dexcap_suit.disconnect_all()


if __name__ == '__main__':
    main()
