# DexCap SDK Python API Reference V1.0.0（对应DexCap设备版本V4）

## 1. 常用数据类型

### 1.1 AdapterType(IntEnum)
枚举类型。定义了DexCap设备可使用的与PC进行连接和数据交换的所有方式。如WIREDUSB指通过USB串口进行连接，BLUETOOTH则是通过蓝牙连接。

### 1.2 DeviceType(IntEnum)
枚举类型。定义了DexCap数采设备中所有独立子设备的类型。其中LGlove/RGlove分别表示左/右手套，UpBody表示外骨骼，IMUnit表示腰部IMU。

### 1.3 DexReturn(IntEnum)
枚举类型。用于SDK常用接口函数的返回值，其取值定义了接口函数执行的各种可能的结果。如DEX_SUCCESS表示函数执行成功，DEX_ERROR表示函数执行出错。
DEX_SUCCESS_WITH_INFO表示函数执行结果被认为成功，但某些步骤或部分模块/子设备的/数据的状态不符合预期，且不影响使用。而DEX_INVALID_DEVICE
则表明被执行的设备(或子设备)对象不可用或不可识别。

### 1.4 GloveJointAngles(ctypes.Structure)
ctypes结构体(types.Structure)。用于封装DexCap手套所有关节角度传感器原始读数，并带有时间戳的结构体，每个关节角度传感器的原始读数均为无符号short，
取值范围为[0, 36000]，对应角度[0.0, 360.0]，即原始读数/100即为角度值。

### 1.5 BodyJointAngles(ctypes.Structure)
ctypes结构体(types.Structure)。用于封装DexCap外骨骼所有关节角度传感器原始读数，并带有时间戳的结构体。每个关节角度传感器的原始读数均为无符号short，
取值范围为[0, 36000]，对应角度[0.0, 360.0]，即原始读数/100即为角度值。

### 1.6 InetMUData(ctypes.Structure)
ctypes结构体(types.Structure)。用于封装IMU数据，并带有时间戳的结构体。其中temperature为IMU温度，poseData为长度为17的float数组，具体字段分别为：
roll，pitch，yaw三轴，四元数，加速度，角速度，磁力计读数（详见C++ SDK的typedef.h中InertialUnitData的声明）

### 1.7 DexCapJointData(ctypes.Structure)
ctypes结构体(types.Structure)。用于整包封装DexCap全套设备(DexCapSuit)所有关节角度等数据，并带有统一同步后时间戳的结构体。

### 1.8 DexCapEndPoses(ctypes.Structure)
ctypes结构体(types.Structure)。DexCap外骨骼双臂末端位姿数据。EndPoseData为4x4矩阵。

### 1.9 MainBatteryState(ctypes.Structure)
ctypes结构体(types.Structure)。DexCap外骨骼主电池的状态数据。
<br><br>

## 2. 常用用户接口

DexCap Python SDK的用于管理DexCap设备和访问设备数据的所有用户接口均依托DexCapSuit类。该类加载并调用DexCap C++ SDK的动态库对应的函数接口完成对应功能。

### 2.1 构造DexCapSuit对象
DexCapSuit构造函数接受一个AdapterType对象adapter_type作为参数，该DexCapSuit对象中所有的设备均须使用adapter_type所指定的连接方式与PC进行连接。

### 2.2 DexCapSuit.is_available()
判断该DexCap套设备对象是否为一个可用对象。通常DexCapSuit对象在构造时会相应的调用底层C++库创建一个DexCapSuit实例并返回其句柄，创建成功后则DexCapSuit对象
即被视为有效对象。若创建时所给定的AdapterType不适用于当前版本的设备，或由于系统资源错误引起的内存分配出错等，DexCapSuit实例将无法创建成功。

### 2.3 DexCapSuit.get_adapter_type()
获取当前DexCapSuit对象创建时指定的连接方式。<br>
**返回值**：AdapterType

### 2.4 DexCapSuit.connect_device()
连接adapter_name所指定的设备，并在连接成功后，自动读取该设备的类型信息，并返回该设备的类型值。<br>
**参数**:
- adapter_name。通常为系统枚举的串口设备地址，或蓝牙设备的名称。
- adapter_type。指定要连接的设备所使用的连接方式，通常与DexCapSuit实例创建时所使用类型一致，若不一致，第一个经该函数成功连接的设备的连接方式将覆盖DexCapSuit实例创建时所指定的连接方式。
- force_glove_charge。设备连接时，是否强制开启外骨骼主电池对DexCap手套进行充电。当连接的设备是DexCap手套时，SDK自动判断当前DexCapSuit实例中外骨骼是否已经连接，并根据该参数的值决定是否开启充电。当连接的设备是外骨骼时，SDK自动判断当前DexCapSuit实例中是否有手套连接，并根据该参数值决定是否开启充电。
<br>

**返回值**：DeviceType。设备连接成功后SDK从该设备固件上读取到的设备类型值


### 2.5 DexCapSuit.disconnect_device()
将指定的设备与SDK的连接断开，设备断开时，SDK将主动对设备进行关传感器使能和关闭采样数据上报的操作，完成后，SDK将不再读取设备的采样数据。<br>
**参数**:
- device。将要断开的设备的类型。
<br>

**返回值**：DexReturn。设备成功断开后，返回DEX_SUCCESS，若断开失败，则返回DEX_ERROR。若设备在断开过程中未能成功将传感器使能关闭，或未能将采样上报关闭，该函数返回DEX_SUCCESS_WITH_INFO。此时建议用户关闭设备电源，以确保下次使用时设备处于正确状态。当返回DEX_SUCCESS_WITH_INFO时，可通过调用get_device_diagnostics()函数来获取具体的错误信息。


### 2.6 DexCapSuit.disconnect_all()
断开当前DexCapSuit实例中所有设备，设备断开后，SDK将不再读取设备的采样数据。<br>

**返回值**：DexReturn。全部设备成功断开后，返回DEX_SUCCESS。若有部分设备未成功断开，或部分设备未能下使能或未能关闭采样上报，则返回DEX_SUCCESS_WITH_INFO。若所有设备均未能断开，则返回DEX_ERROR。

### 2.7 DexCapSuit.is_device_connected()
判断当前DexCapSuit实例中指定的设备是否已连接。<br>
**参数**:
- device。需要判断是否已经连接的设备。
<br>

**返回值**：bool。若指定的设备已连接，返回True，若指定的设备未连接，则返回False。

### 2.8 DexCapSuit.start_sampling()
使当前DexCapSuit实例中的所有DexCap设备启动数据采样并上报。<br>

**返回值**：DexReturn。成功返回DEX_SUCCESS，失败返回DEX_ERROR，部分设备失败则返回DEX_SUCCESS_WITH_INFO.

### 2.9 DexCapSuit.start_device_sampling()
使当前DexCapSuit实例中的指定的设备启动数据采样并上报。<br>
**参数**:
- device。指定的DexCap设备。
<br>

**返回值**：DexReturn。成功返回DEX_SUCCESS，失败返回DEX_ERROR。

### 2.10 DexCapSuit.is_device_sampling()
判断当前DexCapSuit实例中的指定设备的数据采样及上报是否已经开启。<br>
**参数**:
- device。指定的DexCap设备。
<br>

**返回值**：bool。已开启即返回True，否则返回False。


### 2.11 DexCapSuit.stop_sampling()
使当前DexCapSuit实例中的所有DexCap设备全部停止数据采样及上报。<br>
**参数**:
- device。指定的DexCap设备。
<br>

**返回值**：DexReturn。成功返回DEX_SUCCESS，失败返回DEX_ERROR，部分设备失败则返回DEX_SUCCESS_WITH_INFO.

### 2.12 DexCapSuit.stop_device_sampling()
使当前DexCapSuit实例中的指定的设备关闭数据采样及上报。<br>
**参数**:
- device。指定的DexCap设备。
<br>

**返回值**：DexReturn。成功返回DEX_SUCCESS，失败返回DEX_ERROR。

### 2.13 DexCapSuit.get_l_glove_data()
获取当前DexCapSuit实例中的左手套当前时刻的关节数据。<br>

**返回值**：(bool, GloveJointAngles)。成功返回True及左手套的关节数据，失败返回False，且GloveJointAngles中的数据无效。

### 2.14 DexCapSuit.get_r_glove_data()
获取当前DexCapSuit实例中的右手套当前时刻的关节数据。<br>

**返回值**：(bool, GloveJointAngles)。成功返回True及右手套的关节数据，失败返回False，且GloveJointAngles中的数据无效。

### 2.15 DexCapSuit.get_ex_body_data()
获取当前DexCapSuit实例中的外骨骼的上肢关节数据。<br>

**返回值**：(bool, BodyJointAngles)。成功返回True及上肢的关节数据，失败返回False，且BodyJointAngles中的数据无效。

### 2.16 DexCapSuit.get_suit_joint_data()
获取当前DexCapSuit实例中所有设备的状态数据，包括所有关节角度数据，以及IMU数据。<br>

**返回值**：(bool, DexCapJointData)。成功返回True及所有设备的状态数据，失败返回False，且DexCapJointData中的数据无效。

### 2.17 DexCapSuit.get_arms_end_poses()
获取当前DexCapSuit实例中外骨骼左右臂的末端位姿数据。<br>

**返回值**：(bool, DexCapEndPoses)。成功返回True及末端位姿，失败返回False，且DexCapEndPoses中的数据无效。

### 2.18 DexCapSuit.get_l_battery_state()
获取当前DexCapSuit实例左手套电池当前的电压，可以反映电池剩余的电量。通常当电池压低于3.4v后，传感器时效，低于3.5v即有教高概率导致传感器数据失真。<br>

**返回值**：int。电池当前电压*1000。

### 2.19 DexCapSuit.get_r_battery_state()
获取当前DexCapSuit实例右手套电池当前的电压，可以反映电池剩余的电量。通常当电池压低于3.4v后，传感器时效，低于3.5v即有教高概率导致传感器数据失真。<br>

**返回值**：int。电池当前电压*1000。

### 2.20 DexCapSuit.get_main_battery_state()
获取当前DexCapSuit实例中外骨骼主电池的状态数据。<br>

**返回值**：(bool, MainBatteryState)。成功返回True及主电池状态数据，失败返回False，且MainBatteryState中的数据无效。


### 2.21 DexCapSuit.charge_l_glove()
利用当前DexCapSuit实例中外骨骼主电池对左手套进行充电/停止充电，该指令只有在左手套与外骨骼均已连接时才有效。<br>
**参数**:
- charge_on。为True时进行充电，为False时停止充电。
<br>
**返回值**：int，实际为DexReturn。成功返回DEX_SUCCESS，失败返回DEX_ERROR，任一设备未连接时返回DEX_INVALID_DEVICE。

### 2.22 DexCapSuit.charge_r_glove()
利用当前DexCapSuit实例中外骨骼主电池对右手套进行充电/停止充电，该指令只有在右手套与外骨骼均已连接时才有效。<br>

**参数**:
- charge_on。为True时进行充电，为False时停止充电。
<br>
**返回值**：int，实际为DexReturn。成功返回DEX_SUCCESS，失败返回DEX_ERROR，任一设备未连接时返回DEX_INVALID_DEVICE。

### 2.23 DexCapSuit.vibrate_l_motors()
向当前DexCapSuit实例中左手套的各指尖震动电机发送震动指令。<br>

**参数**:
- vib_data。长度为5的uint8数组，分别代表从大拇指到小指的指尖电机的震动强度。震动强度取值范围为[0, 255]
<br>
**返回值**：int，实际为DexReturn。成功返回DEX_SUCCESS，失败返回DEX_ERROR，任一设备未连接时返回DEX_INVALID_DEVICE。

### 2.24 DexCapSuit.vibrate_r_motors()
向当前DexCapSuit实例中右手套的各指尖震动电机发送震动指令。<br>

**参数**:
- vib_data。长度为5的uint8数组，分别代表从大拇指到小指的指尖电机的震动强度。震动强度取值范围为[0, 255]
<br>
**返回值**：int，实际为DexReturn。成功返回DEX_SUCCESS，失败返回DEX_ERROR，任一设备未连接时返回DEX_INVALID_DEVICE。

### 2.25 DexCapSuit.get_diagnostics()
获取当前DexCapSuit实例中的最新诊断信息。通常最新的诊断信息为实例中最后一条执行出错的指令的错误信息，或设备主动上报的最新的错误信息<br>

**返回值**：(int, str)。错误码及详细错误信息文本。

### 2.26 DexCapSuit.get_device_diagnostics()
获取当前DexCapSuit实例中指定设备的最新诊断信息。通常最新的诊断信息为实例中对该设备最后一条执行出错的指令的错误信息，或该设备主动上报的最新的错误信息<br>

**参数**:
- device。指定的DexCap设备。
<br>

**返回值**：(int, str)。错误码及详细错误信息文本。
