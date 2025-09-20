import sys, os, json, importlib

# --- Fix import so Python dùng đúng PyQt6 package ---
QtWidgets = importlib.import_module("PyQt6.QtWidgets")
QtCore = importlib.import_module("PyQt6.QtCore")

QApplication = QtWidgets.QApplication
QWidget = QtWidgets.QWidget
QMainWindow = QtWidgets.QMainWindow
QVBoxLayout = QtWidgets.QVBoxLayout
QHBoxLayout = QtWidgets.QHBoxLayout
QTextEdit = QtWidgets.QTextEdit
QLineEdit = QtWidgets.QLineEdit
QPushButton = QtWidgets.QPushButton
QLabel = QtWidgets.QLabel
QSlider = QtWidgets.QSlider
QComboBox = QtWidgets.QComboBox
QDialog = QtWidgets.QDialog
QFormLayout = QtWidgets.QFormLayout
QDialogButtonBox = QtWidgets.QDialogButtonBox

Qt = QtCore.Qt

# --- Settings state ---
SETTINGS_FILE = "src/settings.json"
current_theme = "Light"
font_size = 14
current_version_type = "beta"
current_lang = "en"


def save_settings():
    settings = {
        "theme": current_theme,
        "text_size": font_size,
        "version": current_version_type
    }
    os.makedirs("src", exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)


def load_settings():
    global current_theme, font_size, current_version_type, current_lang
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                current_theme = data.get("theme", "Light")
                font_size = data.get("text_size", 14)
                current_version_type = data.get("version", "beta")
        except json.JSONDecodeError:
            pass
    current_lang = "en" if current_version_type == "beta" else "enTest"


def get_chatbot_response(user_input: str) -> str:
    try:
        lang_module = importlib.import_module(f"src.langs.{current_lang}")
        return lang_module.get_reply(user_input)
    except ImportError:
        return f"Language file for '{current_lang}' not found."


# --- Settings Dialog ---
class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")

        layout = QFormLayout(self)

        # Theme
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        self.theme_combo.setCurrentText(current_theme)
        layout.addRow("Theme:", self.theme_combo)

        # Version
        self.version_combo = QComboBox()
        self.version_combo.addItems(["beta", "pre-beta"])
        self.version_combo.setCurrentText(current_version_type)
        layout.addRow("Version:", self.version_combo)

        # Text size
        self.size_slider = QSlider(Qt.Orientation.Horizontal)
        self.size_slider.setRange(12, 32)
        self.size_slider.setValue(font_size)
        layout.addRow("Text Size:", self.size_slider)

        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def accept(self):
        global current_theme, font_size, current_version_type, current_lang
        current_theme = self.theme_combo.currentText()
        font_size = self.size_slider.value()
        current_version_type = self.version_combo.currentText()
        current_lang = "en" if current_version_type == "beta" else "enTest"
        save_settings()
        super().accept()


# --- Main Window ---
class LockChatApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 testrun")
        self.setGeometry(100, 100, 1000, 700)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Chat box
        self.chatbox = QTextEdit()
        self.chatbox.setReadOnly(True)
        self.chatbox.setStyleSheet(f"font-size: {font_size}px;")
        main_layout.addWidget(self.chatbox)

        # Input row
        input_layout = QHBoxLayout()
        self.input_entry = QLineEdit()
        self.input_entry.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_entry)

        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_btn)

        self.settings_btn = QPushButton("⚙ Settings")
        self.settings_btn.clicked.connect(self.open_settings)
        input_layout.addWidget(self.settings_btn)

        main_layout.addLayout(input_layout)

    def add_message(self, sender, msg, align=Qt.AlignmentFlag.AlignLeft):
        cursor = self.chatbox.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        fmt = cursor.blockFormat()
        fmt.setAlignment(align)
        cursor.setBlockFormat(fmt)
        cursor.insertText(f"{sender}: {msg}\n")
        self.chatbox.setTextCursor(cursor)
        self.chatbox.ensureCursorVisible()

    def send_message(self):
        user_msg = self.input_entry.text().strip()
        if not user_msg:
            return
        self.input_entry.clear()

        self.add_message("You", user_msg, align=Qt.AlignmentFlag.AlignRight)
        bot_reply = get_chatbot_response(user_msg)
        self.add_message("Bot", bot_reply, align=Qt.AlignmentFlag.AlignLeft)

    def open_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec():
            # Apply font size after settings saved
            self.chatbox.setStyleSheet(f"font-size: {font_size}px;")


if __name__ == "__main__":
    load_settings()
    app = QApplication(sys.argv)
    window = LockChatApp()
    window.show()
    sys.exit(app.exec())
