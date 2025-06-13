import os
import shutil
import json

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')

def get_local_install_path():
    return os.path.expanduser('~/.neonkey')

def install_to_local():
    target = get_local_install_path()
    os.makedirs(target, exist_ok=True)
    for folder in ('scripts', 'assets'):
        src = os.path.join(os.path.dirname(os.path.dirname(__file__)), folder)
        dst = os.path.join(target, folder)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    config['installed'] = True
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"Installed NEONKEY Console to {target}")
