# Import dependencies
from utils import show_message
from PySide6.QtCore import QSettings
from settings_ui import Ui_SettingsDialog
from PySide6.QtWidgets import QDialog, QFileDialog


class SettingsApp(QDialog):
    def __init__(self):
        super().__init__()

        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)

        self.ui.currentFeatures.appendPlainText('\n')

        self.currentFeatures = []
        self.featuresLoaded = False

        self.settings_obj = QSettings("./config/default.ini", QSettings.Format.IniFormat)
        
        if not self.featuresLoaded:
            self.set_features()
        else:
            pass

        # Connection to widgets
        self.ui.addFeatureBtn.clicked.connect(self.add_feature)
        self.ui.createBtn.clicked.connect(self.create_profile)
        self.ui.apply_feature_btn.clicked.connect(self.write_features)
        self.ui.reset_features_btn.clicked.connect(self.reset_features)

    """
    add_feature

    Adds new feature to the list and removes the selected
    one from the combo box.
    """
    def add_feature(self):
        if len(self.currentFeatures) >= 6:
            show_message("info", "SA01: Cannot add more than 6 features.")
        else:
            feature_name = self.ui.featuresBox.currentText()
            if feature_name in self.currentFeatures:
                show_message("error", f"{feature_name} is already present in the list")
            else:
                self.ui.featuresBox.removeItem(self.ui.featuresBox.currentIndex())
                self.currentFeatures.append(feature_name)
                self.ui.currentFeatures.appendPlainText(f"{feature_name}")

    """
    create_profile

    Create profiles for data manager.
    """
    def create_profile(self):

        file_dialog = QFileDialog.getSaveFileName(self, "Save Location", ".")
        if file_dialog[0] == "":
            pass
        else:
            try:
                self.settings_obj_temp = QSettings(file_dialog[0], QSettings.Format.IniFormat)
                self.settings_obj_temp.setValue("general/host", self.ui.hostManagerInput.text())
                self.settings_obj_temp.setValue("general/port", self.ui.portManagerInput.text())
                self.settings_obj_temp.setValue("general/topic_pub", self.ui.publishingTopicLineEdit.text())
                self.settings_obj_temp.setValue("general/topic_sub", self.ui.subscriptionTopicLabel.text())

            except Exception as error:
                show_message("error", str(error))

    """
    write_features

    Write features to config file. Later to be read by the main app instance.
    """
    def write_features(self):
        for i in range(len(self.currentFeatures)):
            self.settings_obj.setValue(f"features/{i}", self.currentFeatures[i])
        self.accept()

    """
    set_features

    Read the features option from ini file and set it to current feautures QPlainTextEdit
    """
    def set_features(self):
        for i in range(0, 6):
            val = self.settings_obj.value(f"features/{i}")
            if val != "":
                self.currentFeatures.append(val)
                self.ui.currentFeatures.appendPlainText(val)
            else:
                pass
        self.featuresLoaded = True

    """
    reset_features

    Remove the currently added features and append them back into combo box
    Also remove features from INI file.
    """
    def reset_features(self):
        for i in range(0, len(self.currentFeatures)):
            self.settings_obj.setValue(f"features/{i}", "")
            self.ui.featuresBox.addItem(self.currentFeatures[i])
        self.ui.currentFeatures.clear()
        self.ui.currentFeatures.setPlainText("Current Features: \n")
        self.currentFeatures = []


def open_settings():
    app = SettingsApp()
    app.show()
    return app.exec()
