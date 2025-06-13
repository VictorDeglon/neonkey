# neonkey

NEONKEY Console is a portable hacker-style hub with neon themed UI.

## Dependencies

Install the required packages with:

```bash
pip install -r requirements.txt
```

## Running

```bash
python3 neonkey.py
```

## Background Watchers

- `USBWatcher.py` launches the console automatically when a NEONKEY USB stick is inserted.
- `ThemeWatcher.py` applies the hacker theme while the drive is connected and restores the desktop when it is removed. Wallpapers are generated on the fly using Pillow so no binary files are stored in the repository.

### Building Windows Binaries

Use [PyInstaller](https://www.pyinstaller.org/) to create standalone executables:

```bash
pyinstaller --onefile USBWatcher.py
pyinstaller --onefile ThemeWatcher.py
```

Copy the generated EXE files onto your NEONKEY USB to run the watchers without needing Python installed.
