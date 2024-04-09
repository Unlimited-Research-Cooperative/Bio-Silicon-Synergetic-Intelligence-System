# This Python file uses the following encoding: utf-8
import sys
from json import dump
from webbrowser import open_new_tab
from PySide6.QtCore import QSettings
from PySide6.QtGui import QIcon
from threading import Thread
from data_manager import DataManager
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QFileDialog, QDialog
from compute_signals import create_transformation, generate_transformed_signals
from window import Ui_MainWindow
import matplotlib.pyplot as plt
from util import get_features, update_vals, read_extra_config
from signals_param import Ui_signalParams


class SignalsParamDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_signalParams()
        self.ui.setupUi(self)

    def show_(self):
        exit_code = self.exec()

        if exit_code == 1:
            with open("./config/extra.json", "w") as signals_param:
                params = {
                    "num_signals": int(self.ui.numSignalInput.text()),
                    "bit_depth": int(self.ui.bit_depth_input.text()),
                    "duration": float(self.ui.durationLineEdit.text()),
                    "fs": float(self.ui.fs_input.text())
                }
                dump(params, signals_param)
                signals_param.close()

        elif exit_code == 0:
            pass

        return exit_code

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.signals_param_dialog = SignalsParamDialog()

        self.setWindowTitle("Signals Simulator")
        self.setWindowIcon(QIcon("./icons/icon.png"))

        self.features = get_features()

        # Connect with buttons
        self.ui.clear_all_btn.clicked.connect(self.clearAll)

        # Connect with actions
        self.ui.actionSave_Config.triggered.connect(self.update_values)
        self.ui.actionExport_Config.triggered.connect(self.save_config)
        self.ui.actionLoad_Config.triggered.connect(self.load_config)
        self.ui.actionGitHub.triggered.connect(self.open_github)
        self.ui.actionParameters.triggered.connect(self.open_param_info)
        self.ui.actionAbout.triggered.connect(self.open_docs)
        self.ui.simulate_btn.clicked.connect(self.simulate)

    def open_github(self):
        open_new_tab("https://github.com/Unlimited-Research-Cooperative/Bio-Silicon-Synergetic-Intelligence-System")

    def open_docs(self):
        open_new_tab("https://raghav67816.github.io/urc.bssis.github.io/")

    def open_param_info(self):
        open_new_tab("https://raghav67816.github.io/urc.bssis.github.io/Tools/Signal%20Simulator/")


    # Clear all fields
    def clearAll(self):
        for widget in self.findChildren(QLineEdit):
            widget.clear()

    # Get all inputs
    def get_all_input(self):
        vals = []
        for widget in self.findChildren(QLineEdit):
            vals.append(widget.text())
        return vals
    
    # Update all features in the file
    def update_values(self):
        vals = self.get_all_input()
        update_vals(self.features, vals)


    # Load config from a file
    def load_config(self):
        config_path = QFileDialog.getOpenFileName(self, "Load Configuration File", filter="*.ini")
        if config_path[0] == "":
            pass
        else:
            new_settings_obj = QSettings(config_path[0], QSettings.Format.IniFormat)
            loaded_vals = []
            widgets = []

            for i in range(0, len(self.features)):
                loaded_vals.append(new_settings_obj.value(f"features/{self.features[i]}"))

            for widget in self.findChildren(QLineEdit):
                widgets.append(widget)

            for x in range(0, len(widgets)):
                widgets[x].setText(loaded_vals[x])


    # Save config
    def save_config(self):
        try:
            config_file_path = QFileDialog.getSaveFileName(self, "Save Config", ".", "*.ini")
            if config_file_path[0] == '':
                pass
            else:
                with open('./config/config.ini') as default_config:
                    conf = default_config.read()
                    default_config.close()

                with open(config_file_path[0], "w") as config_file:
                    config_file.write(conf)
                    config_file.close()
        
        except Exception as e:
            print(e)

    def plot_separate_signals(self, signals, title_prefix):
        num_signals = signals.shape[0]
        plt.figure(figsize=(15, num_signals * 5))  # Adjust figure size to make each subplot 5 times taller
        plt.style.use('dark_background')

        for i in range(num_signals):
            ax = plt.subplot(num_signals, 1, i+1)
            ax.plot(signals[i], color='red', linewidth=0.4)
            ax.set_title(f'{title_prefix} Signal {i+1}', color='red')
            ax.set_ylabel('Amplitude', color='red')
            ax.tick_params(axis='x', colors='red')
            ax.tick_params(axis='y', colors='red')
            ax.grid(True, which='both', color='red', linestyle='-', linewidth=0.2)
            for spine in ax.spines.values():
                spine.set_edgecolor('red')

            plt.savefig(f"./Transformed Signal {i+1}.png")

        # Adjust the spacing between subplots
        plt.subplots_adjust(hspace=0.1)  # You can adjust this value as needed

    def plot_graphs(self, transformed_signals):
        graph_thread = Thread(target=self.plot_separate_signals, args=[transformed_signals, "Transformed"])
        graph_thread.daemon = True
        graph_thread.start()
    
    def simulate(self):
        try:
            code = self.signals_param_dialog.show_()
            if code == 1:
                data_m = DataManager("signals_simulator", None, "signals")
                extra_config = read_extra_config()
                # bit_depth = extra_config['bit_depth'] 
                duration = extra_config['duration']
                fs = extra_config['fs']
                num_signals = extra_config['num_signals']

                lenght = fs*duration
                transformations = create_transformation()
                trasnformed_signals = generate_transformed_signals(lenght, num_signals, transformations)
                data_m.set_data(str(trasnformed_signals))
                data_m.publish(1)
                self.plot_separate_signals(trasnformed_signals, "Transformed")

            else:
                pass

        except Exception as simulation_error:
            print(str(simulation_error))
            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Signal Simulator")
    app.setOrganizationName("Synthetic Intelligence Labs")
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
