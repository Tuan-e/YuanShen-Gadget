import ctypes
import time
import sys
from ctypes import wintypes
from PIL import ImageGrab

user32 = ctypes.WinDLL("user32")
shell32 = ctypes.WinDLL("shell32")
user32.SetProcessDPIAware(2)


def mouse(x: int, y: int):
    user32.SetCursorPos(x, y)
    user32.mouse_event(0x2)
    user32.mouse_event(0x4)


def blank():
    user32.keybd_event(32, 0, 0, 0)
    user32.keybd_event(32, 0, 2, 0)


def get_hwnd(title) -> int:
    return user32.FindWindowW(0, title)


def ys_win(h: int) -> tuple:
    rect = wintypes.RECT()
    user32.GetWindowRect(h, ctypes.pointer(rect))
    return rect.left, rect.top, rect.right, rect.bottom


def graphic(bbox: tuple, target_color=(236, 229, 216)) -> bool:
    x, y = bbox[0], bbox[1]
    discern_x, discern_y = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tmp = ImageGrab.grab(
        bbox=(x + discern_y * 0.048, y + discern_x * 0.036, x + discern_y * 0.082, y + discern_x * 0.058))
    width, height = tmp.size
    count = 0
    for y in range(height):
        for x in range(width):
            pixel_color = tmp.getpixel((x, y))
            if pixel_color == target_color:
                count += 1
    print(count, '\t', end='')
    return count > 20


def main():
    screen = user32.GetSystemMetrics
    hwnd = get_hwnd('原神')
    user32.ShowWindow(hwnd, 9)
    print('当前主屏幕分辨率：', screen(0), screen(1))
    t = 0
    win = ys_win(hwnd)
    while True:
        t += 1
        if t == 10:
            hwnd = get_hwnd('原神')
            if hwnd != 0:
                win = ys_win(hwnd)
                print("Get window")
                t = 0
            else:
                user32.MessageBoxW(0, '原神已关闭！', 'YuanShen Tools', 0x0)
                exit()
        if hwnd == user32.GetForegroundWindow():
            if graphic(win):
                blank()
                print("succeed")
                time.sleep(0.08)
            else:
                print("waiting......")
                time.sleep(0.3)
        else:
            print("Unselected window......")
            time.sleep(0.5)


if __name__ == '__main__':
    g = get_hwnd('原神')
    if g == 0:
        user32.MessageBoxW(0, '请启动原神并关闭启动器！', 'YuanShen Tools', 0x0)
        exit()
    else:
        if shell32.IsUserAnAdmin():
            main()
        else:
            shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            exit()
