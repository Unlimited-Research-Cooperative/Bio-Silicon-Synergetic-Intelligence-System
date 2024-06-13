from time import sleep
from thread_manager import ThreadManager
from processes_dialog import Ui_RunningThreads
from PySide6.QtWidgets import QDialog, QApplication, QTableWidgetItem

class ThreadApp(QDialog):
    def __init__(self, running_services: ThreadManager):
        super().__init__()

        self.ui = Ui_RunningThreads()
        self.ui.setupUi(self)

        self.manager = running_services

        self.ui.pushButton.clicked.connect(self.terminate_thread)

        self.services = running_services.services
        for index, services in enumerate(self.services):
            self.ui.tableWidget.insertRow(index)
            item = QTableWidgetItem()
            item.setText(self.services[services].service_name)
            self.ui.tableWidget.setItem(index, 0, item)

        for index, services in enumerate(self.services):
            thread_id_item = QTableWidgetItem()
            thread_id_item.setText(str(self.services[services].thread_id))
            self.ui.tableWidget.setItem(index, 1, thread_id_item)

        for index, services in enumerate(self.services):
            status_item = QTableWidgetItem()
            status_item.setText("Running")
            self.ui.tableWidget.setItem(index, 2, status_item)


    def terminate_thread(self):
        selected_item = self.ui.tableWidget.selectedItems()
        self.manager.kill_thread(selected_item[0].text())

def run_app(manager: ThreadManager):
    app_ = QApplication()
    app = ThreadApp(manager)
    app.show()
    app.exec()
