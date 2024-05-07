# Import dependencies
from sys import exit, argv
from app_ui import Ui_MainWindow
from PySide6.QtCore import QSettings
from settings_app import open_settings
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel


class UnifiedApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.settings_obj = QSettings("./config/default.ini", QSettings.Format.IniFormat)

        self.featureDisplayed = False

        self.ui.settingsBtn.clicked.connect(self.handle_settings_app)

    # handle settings dialog events
    def handle_settings_app(self):
        dialog_exec = open_settings()
        if dialog_exec == 1:
            self.add_features_to_display()
        else:
            pass

    
    """
    add_features_to_display

    Adds features to "Extracted Featuers" group box.
    """
    def add_features_to_display(self):
        self.clear_features()
        if not self.featureDisplayed:
            features = []
            for i in range(0, 6):
                val = self.settings_obj.value(f"features/{i}")
                if val != "":
                    features.append(val)

                    obj_name_label = val.lower().replace(" ", "_")

                    label_widget = QLabel(self)
                    value_widget = QLabel(self)

                    label_widget.setText(val)
                    label_widget.setObjectName(f"{obj_name_label}_label")

                    value_widget.setText("--")
                    value_widget.setObjectName(f"{obj_name_label}_val")

                    self.ui.extFeaturesLayout.addRow(label_widget, value_widget)

                self.ui.extFeaturesLayout.setHorizontalSpacing(20)
                self.ui.extFeaturesLayout.setVerticalSpacing(10)
                self.featureDisplayed = True
        else:
            pass

    """
    clear_features

    Remove all features
    """
    def clear_features(self):
        labels = self.ui.extFeaturesGBox.findChildren(QLabel)
        if len(labels) == 0:
            pass

        else:
            for label in labels:
                label.deleteLater()
            self.featureDisplayed = False


app = QApplication(argv)
window = UnifiedApp()
window.show()
exit(app.exec())
