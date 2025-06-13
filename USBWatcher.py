import os
import time
import subprocess
import psutil
import ctypes

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MARKER_PATH = os.path.join('NEONKEY', 'launch.flag')
EXECUTABLE = 'NEONKEY_Console.exe'
SCRIPT = 'neonkey.py'
KNOWN_LABELS = {'NEONKEY'}


def list_drives():
    return [p.device for p in psutil.disk_partitions(all=False)]


def get_volume_label(drive):
    if os.name == 'nt':
        buf = ctypes.create_unicode_buffer(1024)
        if ctypes.windll.kernel32.GetVolumeInformationW(ctypes.c_wchar_p(drive), buf, ctypes.sizeof(buf), None, None, None, None, 0):
            return buf.value.strip()
    return ''


def launch_from_drive(drive):
    marker = os.path.join(drive, MARKER_PATH)
    if os.path.exists(marker) or get_volume_label(drive).upper() in KNOWN_LABELS:
        exe = os.path.join(drive, EXECUTABLE)
        script = os.path.join(drive, SCRIPT)
        if os.path.exists(exe):
            if os.name == 'nt':
                os.startfile(exe)
            else:
                subprocess.Popen([exe])
            return True
        if os.path.exists(script):
            cmd = ['python', script] if os.name == 'nt' else ['python3', script]
            subprocess.Popen(cmd)
            return True
    return False


def main():
    print('USBWatcher running...')
    known = set(list_drives())
    while True:
        time.sleep(2)
        drives = set(list_drives())
        added = drives - known
        for d in added:
            if launch_from_drive(d):
                print(f'Launched NEONKEY from {d}')
        known = drives


if __name__ == '__main__':
    main()
