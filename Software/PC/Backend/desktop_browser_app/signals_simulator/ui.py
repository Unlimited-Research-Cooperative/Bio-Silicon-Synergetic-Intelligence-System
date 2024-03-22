# This Python file uses the following encoding: utf-8
import sys
from webbrowser import open_new_tab
from numpy.random import uniform
from PySide6.QtCore import QSettings
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QFileDialog, QMessageBox
from compute_signals import create_transformation, generate_transformed_signals, plot_separate_signals
from ui_form import Ui_MainWindow
from util import get_features, update_vals


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Most used variables
        self.min_volt = None
        self.max_volt = None

        self.setWindowTitle("Signal Simulator")
        self.setWindowIcon(QIcon("signal_simulator/icons/icon.png"))

        self.features = get_features()
        self.loaded_config_obj = None

        self.ui.clear_all_btn.clicked.connect(self.clear_all)
        self.ui.simulate_btn.clicked.connect(self.simulate)

        self.ui.actionLoad_Config.triggered.connect(self.load_config)
        self.ui.actionsave_values.triggered.connect(self.update_all_vals)
        self.ui.actionGitHub.triggered.connect(self.open_github)
        self.ui.actionSave_Config.triggered.connect(self.save_config)

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

    def load_config(self):
        config_path = QFileDialog.getOpenFileName(self, "Load Configuration File", filter="*.ini")
        if config_path[0] == "":
            pass
        else:
            new_settings_obj = QSettings(config_path[0], QSettings.Format.IniFormat)
            self.min_volt = float(new_settings_obj.value("features/min_volt"))
            self.max_volt = float(new_settings_obj.value("features/max_volt"))
            loaded_vals = []
            widgets = []

            for i in range(0, len(self.features)):
                loaded_vals.append(new_settings_obj.value(f"features/{self.features[i]}"))

            for widget in self.findChildren(QLineEdit):
                widgets.append(widget)

            for x in range(0, len(widgets)):
                widgets[x].setText(loaded_vals[x])

    def save_config(self):
        save_file_path = QFileDialog.getSaveFileName(self, "Save Configuration File", filter="*.ini")
        if save_file_path[0] == "":
            pass

        else:
            vals = self.get_all_input()
            with open(save_file_path[0], "w") as new_config_file:
                new_config_file.writelines("[features]\n")
                for i in range(0, len(vals)):
                    new_config_file.write(f"{self.features[i]}={vals[i]}\n")
                new_config_file.close()
                print("done")

    def open_github(self):
        open_new_tab(
            "https://github.com/Unlimited-Research-Cooperative/Bio-Silicon-Synergetic-Intelligence-System/tree/main")

    def simulate(self):
        bit_depth = 16
        num_signals = 32
        fs = 500
        duration = 1
        length = fs * duration

        transformations = create_transformation()
        transformed_signals = generate_transformed_signals(length, num_signals, transformations)
        plot_separate_signals(transformed_signals, "Transformed")

        ecog_data = [uniform(self.min_volt, self.max_volt) for _ in range(num_signals)]
        print(ecog_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Signal Simulator")
    app.setOrganizationName("URC")
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
