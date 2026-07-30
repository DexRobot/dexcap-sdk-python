import time
from time import sleep

from dexcap import *


def main():
    dexcap_suit = DexCapSuit(AdapterType.WIREDUSB)
    if dexcap_suit.is_available() is not True:
        print('DexCapSuit instance created failed')
        return

    wde = WiredDeviceEnumerator()
    dev_candidates_count = wde.number_of_device_candidates()
    print('There are {} USB devices may be DexCap product'.format(dev_candidates_count))

    suit_available = False
    device_candidates = wde.get_device_candidates()
    for adapter_name in device_candidates:
        device_type = dexcap_suit.connect_device(adapter_name, dexcap_suit.get_adapter_type())
        if device_type is DeviceType.UnDefn:
            print('Device {} is not recognized as a DexCap device, either this device is busy, not working or malfunctioning'.format(adapter_name))
            continue

        print('Device {} is connected, Device Type: {}'.format(adapter_name, device_type.name))
        suit_available = True

    if not suit_available:
        return

    return_code = dexcap_suit.start_sampling()
    if return_code is not DexReturn.DEX_SUCCESS and return_code is not DexReturn.DEX_SUCCESS_WITH_INFO:
        print('Sampling starts failed')
        return

    timeout = False
    start_ts = time.time()
    while not timeout:
        res_joint_angles = dexcap_suit.get_suit_joint_data()
        if res_joint_angles[0] is not True:
            continue

        data = res_joint_angles[1]
        if (data.mask & 0x8000) != 0:
            print('[Left Glove]: ', end=' ')
            for idx in range(21):
                print('jnt{}={}, '.format(idx, data.LGlove[idx]), end='')
            print('')

        if (data.mask & 0x4000) != 0:
            err_code, err_info = dexcap_suit.get_device_diagnostics(DeviceType.UpBody)
            if err_code != 0:
                print('[ERROR]-[UpBody]: Error Code={}, Error Info=\'{}\''.format(err_code, err_info))
            print('[Exo UpBody]: ', end=' ')
            for idx in range(23):
                print('jnt{}={}, '.format(idx, data.ExBody[idx]), end='')
            print('')

        if (data.mask & 0x2000) != 0:
            print('[Right Glove]: ', end=' ')
            for idx in range(21):
                print('jnt{}={}, '.format(idx, data.RGlove[idx]), end='')
            print('')

        print('=============================================')

        # vib_data = [100, 100, 0, 0, 0]
        # dexcap_suit.vibrate_l_motors(vib_data)
        duration = time.time() - start_ts
        timeout = duration >= 30
        sleep(0.1)

    dexcap_suit.disconnect_all()


if __name__ == '__main__':
    main()
