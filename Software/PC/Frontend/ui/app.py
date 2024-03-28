import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import Qt, QObject, Slot
from PySide6.QtWebEngineWidgets import QWebEngineView


class TestObj(QObject):
    @Slot(str)
    def say_hello(self):
        print("Hello, Moto !")



class AppWindow(QWebEngineView):
    def __init__(self):
        super().__init__()

        # self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setUrl("http://localhost:3000")

        methods = TestObj()
        channel = QWebChannel()
        
        channel.registerObject("backend", methods)
        self.page().setWebChannel(channel)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec())
