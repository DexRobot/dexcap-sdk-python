# DexCap Python SDK

**版本**  V1.0.0

## 1 **概述**
DexCap Python SDK V1.0.0 为DexCap外骨骼数据采集产品的V4版硬件提供了设备识别，连接管理，采集数据读取，功能管理设置，以及反馈控制等编程接口。
为使用DexCap V4外骨骼数采设备的用户提供了基于Python的二次开发能力，开发人员可根据自身应用场景，使用该SDK提供的API接口，实时获取外骨骼设备各
关节的角度数据，以及手臂末端位姿等数据，并通过对所获数据进行实时传输和计算，实现用于AI训练的数据采集，以及实时遥操各类机械臂，灵巧手等设备的功能。

## 2 **安装与使用**

### 2.1 环境要求
Python最低版本要求3.10

### 2.2 获取方式

```
git clone --recursive https://github.com/DexRobot/dexcap-sdk-python.git
```
DexCap Python SDK依赖DexCap的C++ SDK动态库，因而从github上clone代码时，请确保加上--recursive选项。若clone时未加上--recursive选项，可以在clone
完成后，进入dexcap-sdk-python目录，执行如下命令拉取依赖的C++库:
```
git submodule update --init --recursive
```

### 2.3 目录结构

```
dexcap-sdk-python/
├── contrib/                   # 子模块目录，该目录下均为被依赖的外部库，目前仅包含DexCap的C++ SDK
│   ├── dexcap-sdk-cpp/        # DexCap的C++ SDK
├── dexcap/                    # DexCap Python SDK的源代码目录
│   ├── __init__.py            # __init__.py
│   ├── dexcap.py              # DexCap Python SDK的核心代码，包含DexCapSuit类定义和所有的用户接口函数
│   ├── typedefs.py            # DexCap Python SDK的基本数据类型，数据模型，常量等定义
│   ├── utils.py               # 工具类，函数等。如获取可用的串口设备列表（仅DexCap SDK可识别的串口设备）
├── examples/                  # 动态库文件所在目录
│   ├── example.py             # Python示例代码
├── setup.py                   # 安装脚本
```

### 2.4 安装
进入已获取的DexCap Python SDK的目录dexcap-sdk-python，确认setup.py文件存在，执行如下命令：
```
pip install -e .
```
<br><br>

## 3. **API 使用说明**

### [2.1. Python API Reference(中文)](./docs/Python-API-Reference-CHS.md)

