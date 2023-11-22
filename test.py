import pynvml
import ctypes
import sys

shell32 = ctypes.WinDLL("shell32")

if shell32.IsUserAnAdmin():
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    print("GPU数量", pynvml.nvmlDeviceGetCount())
    print("GPU型号", pynvml.nvmlDeviceGetName(handle))
    print("GPU驱动版本", pynvml.nvmlSystemGetDriverVersion())
    info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    print("GPU显存容量", info.total / 1024 ** 2)
    print("GPU已用显存容量", info.used / 1024 ** 2)
    print("GPU剩余显存容量", info.free / 1024 ** 2)
    print("GPU核心温度", pynvml.nvmlDeviceGetTemperature(handle, 0))
    print("GPU供电水平", pynvml.nvmlDeviceGetPowerState(handle))
    print(pynvml.nvmlDeviceGetDriverModel(handle))
    input("回车继续......")
    pynvml.nvmlDeviceSetDriverModel(handle, 1)
    pynvml.nvmlShutdown()
else:
    shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    exit()
