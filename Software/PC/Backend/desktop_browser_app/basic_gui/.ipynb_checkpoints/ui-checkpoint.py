# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtGui import QIcon
from webbrowser import open_new_tab
from PySide6.QtCore import QSettings
from util import get_features, update_vals
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QFileDialog, QMessageBox
from compute_signals import create_transformation, generate_transformed_signals, plot_separate_signals

from ui_form import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Signal Simulator")
        self.setWindowIcon(QIcon("./icon.png"))

        self.features = get_features()

        self.ui.clear_all_btn.clicked.connect(self.clear_all)
        self.ui.simulate_btn.clicked.connect(self.simulate)

        self.ui.actionLoad_Config.triggered.connect(self.load_config)
        self.ui.actionSave_Config.triggered.connect(self.update_all_vals)
        self.ui.actionGitHub.triggered.connect(self.open_github)

    def get_all_input(self):
        vals = []
        for widgets in self.findChildren(QLineEdit):
            vals.append(widgets.text())
        return vals

    def show_error(self, title: str, message: str, detailed: str):
        msg_box = QMessageBox(QMessageBox.Icon.Critical, title, message, QMessageBox.StandardButton.Ok)
        msg_box.setDetailedText(detailed)
        msg_box.show()

    def update_all_vals(self):
        vals = self.get_all_input()
        update_vals(self.features, vals)

    def clear_all(self):
        for widget in self.findChildren(QLineEdit):
            widget.clear()
    
    def saveConfig(self, filename):
        config = {
            "bit_depth": self.bit_depth,
            "num_signals": self.num_signals,
            "fs": self.fs,
            "duration": self.duration,
            "min_volt": self.min_volt,
            "max_volt": self.max_volt
        }
        
    with open(filename, 'w') as f:
        json.dump(config, f)
    def load_config(self):
        config_path = QFileDialog.getOpenFileName(self, "Load Configuration File", filter="*.ini")
        print(config_path[0])
        new_settings_obj = QSettings(config_path[0], QSettings.Format.IniFormat)
        loaded_vals = []
        widgets = []

        for i in range(0, len(self.features)):
            loaded_vals.append(new_settings_obj.value(f"features/{self.features[i]}"))

        for widget in self.findChildren(QLineEdit):
            widgets.append(widget)

        for x in range(0, len(widgets)):
            widgets[x].setText(loaded_vals[x])

    def open_github(self):
        open_new_tab(
            "https://github.com/Unlimited-Research-Cooperative/Bio-Silicon-Synergetic-Intelligence-System/tree/main")

    def simulate(self):
        bit_depth = int(self.ui.bitDepthInput.text())  # Assuming ui.bitDepthInput is your QLineEdit for bit depth
        num_signals = int(self.ui.numSignalsInput.text())
        fs = int(self.ui.samplingFrequencyInput.text())  
        duration = float(self.ui.durationInput.text())
        min_volt = float(self.ui.minVoltInput.text())
        max_volt = float(self.ui.maxVoltInput.text())
        
        length = fs * duration
        transformations = create_transformation()
        transformed_signals = generate_transformed_signals(length, num_signals, transformations, fs, duration, min_volt, max_volt)
        plot_separate_signals(transformed_signals, "Transformed")
            
        print(transformed_signals)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Signal Simulator")
    app.setOrganizationName("Synthetic Intelligence Labs")
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
