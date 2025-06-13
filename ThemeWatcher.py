import os
import time
import json
import ctypes
import psutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WINDOWS = os.name == 'nt'
MARKER_PATH = os.path.join('NEONKEY', 'launch.flag')
BACKUP_FILE = os.path.join(SCRIPT_DIR, 'settings_backup.json')
HACKER_WALLPAPER = os.path.join(SCRIPT_DIR, 'hacker_wallpaper.bmp')
DEFAULT_WALLPAPER = os.path.join(SCRIPT_DIR, 'default_wallpaper.bmp')


def generate_wallpaper(path, theme='hacker'):
    """Create a simple wallpaper image if it doesn't exist."""
    if os.path.exists(path):
        return
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return
    w, h = 1920, 1080
    if theme == 'hacker':
        img = Image.new('RGB', (w, h), 'black')
        draw = ImageDraw.Draw(img)
        for y in range(0, h, 40):
            color = (0, 255, 0)
            draw.line((0, y, w, y), fill=color)
        for x in range(0, w, 40):
            draw.line((x, 0, x, h), fill=(0, 100, 0))
    else:
        img = Image.new('RGB', (w, h), (43, 43, 43))
    img.save(path)

SPI_SETDESKWALLPAPER = 0x0014
SPI_GETDESKWALLPAPER = 0x0073


def list_mounts():
    return [p.mountpoint for p in psutil.disk_partitions(all=False)]


def find_neonkey_drive():
    for m in list_mounts():
        if os.path.exists(os.path.join(m, MARKER_PATH)):
            return m
    return None


def get_wallpaper():
    buf = ctypes.create_unicode_buffer(260)
    if WINDOWS:
        ctypes.windll.user32.SystemParametersInfoW(SPI_GETDESKWALLPAPER, 260, buf, 0)
    return buf.value


def set_wallpaper(path):
    if WINDOWS:
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 3)


def apply_theme(drive):
    current = get_wallpaper()
    with open(BACKUP_FILE, 'w') as f:
        json.dump({'wallpaper': current}, f)
    wp = HACKER_WALLPAPER
    generate_wallpaper(wp, 'hacker')
    set_wallpaper(wp)


def revert_theme():
    if not os.path.exists(BACKUP_FILE):
        return
    with open(BACKUP_FILE) as f:
        data = json.load(f)
    if not os.path.exists(data.get('wallpaper', '')):
        generate_wallpaper(DEFAULT_WALLPAPER, 'default')
        wp = DEFAULT_WALLPAPER
    else:
        wp = data.get('wallpaper')
    set_wallpaper(wp)
    os.remove(BACKUP_FILE)


def main():
    if not WINDOWS:
        print('ThemeWatcher is Windows only')
        return
    print('ThemeWatcher running...')
    active = False
    current_drive = None
    while True:
        drive = find_neonkey_drive()
        if drive and not active:
            apply_theme(drive)
            active = True
            current_drive = drive
            print('Hacker theme applied')
        elif not drive and active:
            revert_theme()
            active = False
            current_drive = None
            print('Theme reverted')
        time.sleep(2)


if __name__ == '__main__':
    main()
