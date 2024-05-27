import sys
import constants
from sys import exit
from dotenv import set_key
from threading import Thread
from data_manager import DataManager
from features_to_game import Executor
from datetime import datetime
from signals_to_features import SignalConverter
from app_ui import Ui_SignalsTranslatorWindow
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.env_path = "./config.env"

        self.ui = Ui_SignalsTranslatorWindow()
        self.ui.setupUi(self)
        
        self.setWindowTitle("Signals Monitor")

        self.ui.translatedOutput.setEnabled(True)
        self.ui.translatedOutput.setReadOnly(True)
        self.ui.msg_label.setWordWrap(True)

        self.executor = None
        self.converter = None
        self.data_m = None
        self.game_inputs = []

        self.setWindowTitle("Signals Translator")
        self.ui.startBtn.clicked.connect(self.start)
        self.ui.export_btn.clicked.connect(self.export_data)

    def start(self):
        host = self.ui.hostLineEdit_2.text()
        port = self.ui.portLineEdit_2.text()

        set_key(self.env_path, "host", str(host))
        set_key(self.env_path, "port", str(port))

        self.ui.hostLineEdit.setText(host)
        self.ui.portLineEdit.setText(port)

        try:
            self.converter = SignalConverter()
            self.run_converter_thread()
            self.run_executor_thread()
            self.data_m = DataManager("Signals Translator", constants.GAME_INPUTS, None, self.append_game_inputs)
            self.data_m.listen()

        except Exception as error:
            self.show_error(str(error))

    def append_game_inputs(self, input_):
        time_now = datetime.now().strftime("%H:%M:%S")
        self.ui.translatedOutput.appendPlainText(f"{time_now}: {input_}")


    def run_converter_thread(self):
        conv_thread = Thread(target=self.converter.data_m.listen)
        conv_thread.start()

    def run_executor_thread(self):
        exec_thread = Thread(target=Executor)
        exec_thread.start()

    def export_data(self):
        file_path = QFileDialog.getOpenFileName(self, "Select path for export file", ".")
        if file_path[0] == '':
            pass

        else:
            print(file_path[0])
            print("Writing data.")
            try:
                with open(str(file_path[0]), "w") as data_file:
                    data_file.write(self.ui.translatedOutput.toPlainText())
                    data_file.close()

            except Exception as export_error:
                self.show_error(str(export_error))
 
    def show_error(self, text: str):
        msg_box = QMessageBox(self)
        msg_box.setText(text)
        msg_box.setWindowTitle("Signals Translator")
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.show()


app = QApplication(sys.argv)
app_window = AppWindow()
app_window.show()
exit(app.exec())
