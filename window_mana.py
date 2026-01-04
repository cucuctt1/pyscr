import os

def get_max_window_size():
    if os.name == 'posix':
        return get_unix_max_window_size()
    elif os.name == 'nt':
        return get_windows_max_window_size()
    else:
        raise OSError("Unsupported operating system")

def get_unix_max_window_size():
    rows, columns = os.popen('stty size', 'r').read().split()
    rows = int(rows) - 1
    return int(columns), int(rows)

def get_windows_max_window_size():
    from ctypes import windll, wintypes, byref

    user32 = windll.user32
    hdc = user32.GetDC(0)
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    user32.ReleaseDC(0, hdc)
    adjusted_height = height-40
    adjusted_width = width
    return adjusted_width,adjusted_height