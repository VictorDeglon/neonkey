import os
import sys
import json
import platform
import psutil
from PyQt5 import QtWidgets, QtCore, QtGui

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')

class InstallDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showFullScreen()
        layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel("Install NEONKEY Console on this machine?")
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)
        btn_yes = QtWidgets.QPushButton("Yes")
        btn_no = QtWidgets.QPushButton("No")
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(btn_yes)
        btn_layout.addWidget(btn_no)
        layout.addLayout(btn_layout)
        btn_yes.clicked.connect(self.accept)
        btn_no.clicked.connect(self.reject)

class SidebarButton(QtWidgets.QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFlat(True)
        self.setCursor(QtCore.Qt.PointingHandCursor)

class Dashboard(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        self.info = QtWidgets.QTextEdit()
        self.info.setReadOnly(True)
        layout.addWidget(self.info)
        self.update_info()

    def update_info(self):
        info_text = [
            f"OS: {platform.system()} {platform.release()}",
            f"CPU: {psutil.cpu_percent()}%",
            f"RAM: {psutil.virtual_memory().percent}%",
            f"Uptime: {int(psutil.boot_time())}",
        ]
        self.info.setPlainText("\n".join(info_text))

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.resize(800, 500)
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        self.sidebar = QtWidgets.QFrame()
        self.sidebar.setFixedWidth(150)
        self.sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar)
        self.sidebar_layout.setAlignment(QtCore.Qt.AlignTop)

        self.stack = QtWidgets.QStackedWidget()

        self.pages = {}
        for name in [
            "Unlock Files",
            "Apply Theme",
            "Launch Tools",
            "Open Vaults",
            "Run Scripts",
            "Security Mode",
            "System Info",
        ]:
            btn = SidebarButton(name)
            self.sidebar_layout.addWidget(btn)
            page = Dashboard() if name == "System Info" else QtWidgets.QLabel(name)
            page.setAlignment(QtCore.Qt.AlignCenter)
            self.stack.addWidget(page)
            idx = self.stack.count() - 1
            btn.clicked.connect(lambda checked, i=idx: self.stack.setCurrentIndex(i))
            self.pages[name] = page

        layout = QtWidgets.QHBoxLayout(central)
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack)
        self.title = QtWidgets.QLabel("NEONKEY Console")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.stack.addWidget(self.title)

        close_btn = QtWidgets.QPushButton('X')
        close_btn.clicked.connect(QtWidgets.qApp.quit)
        close_btn.setFixedSize(30, 30)
        self.sidebar_layout.addWidget(close_btn)

        self.stack.setCurrentIndex(0)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {"theme": "default", "installed": False}


def save_config(cfg):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(cfg, f, indent=2)


def is_running_from_usb():
    path = os.path.abspath(__file__)
    if sys.platform.startswith('win'):
        return path.startswith('D:') or path.startswith('E:')
    return path.startswith('/media') or path.startswith('/mnt')


def apply_theme(app, name):
    theme_path = os.path.join(os.path.dirname(__file__), 'assets', 'themes', f"{name}.qss")
    if os.path.exists(theme_path):
        with open(theme_path) as f:
            app.setStyleSheet(f.read())


def main():
    app = QtWidgets.QApplication(sys.argv)
    cfg = load_config()

    if is_running_from_usb() and not cfg.get('installed'):
        dialog = InstallDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            from scripts.install import install_to_local
            install_to_local()

    apply_theme(app, cfg.get('theme', 'default'))

    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
