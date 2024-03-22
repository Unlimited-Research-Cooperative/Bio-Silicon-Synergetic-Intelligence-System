# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionLoad_Config = QAction(MainWindow)
        self.actionLoad_Config.setObjectName(u"actionLoad_Config")
        self.actionSave_Config = QAction(MainWindow)
        self.actionSave_Config.setObjectName(u"actionSave_Config")
        self.actionChange_Export_Path = QAction(MainWindow)
        self.actionChange_Export_Path.setObjectName(u"actionChange_Export_Path")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionExit.setMenuRole(QAction.QuitRole)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionParameters = QAction(MainWindow)
        self.actionParameters.setObjectName(u"actionParameters")
        self.actionGitHub = QAction(MainWindow)
        self.actionGitHub.setObjectName(u"actionGitHub")
        self.actionsave_values = QAction(MainWindow)
        self.actionsave_values.setObjectName(u"actionsave_values")
        self.actionsave_values.setMenuRole(QAction.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.btn_frame = QFrame(self.centralwidget)
        self.btn_frame.setObjectName(u"btn_frame")
        self.btn_frame.setMinimumSize(QSize(0, 50))
        self.btn_frame.setMaximumSize(QSize(16777215, 50))
        self.btn_frame.setStyleSheet(u"QFrame{\n"
"	border: 0px solid;\n"
"}")
        self.btn_frame.setFrameShape(QFrame.StyledPanel)
        self.btn_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.btn_frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.simulate_btn = QPushButton(self.btn_frame)
        self.simulate_btn.setObjectName(u"simulate_btn")
        self.simulate_btn.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_2.addWidget(self.simulate_btn)

        self.clear_all_btn = QPushButton(self.btn_frame)
        self.clear_all_btn.setObjectName(u"clear_all_btn")
        self.clear_all_btn.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_2.addWidget(self.clear_all_btn)


        self.verticalLayout_3.addWidget(self.btn_frame, 0, Qt.AlignRight)

        self.details_frame = QFrame(self.centralwidget)
        self.details_frame.setObjectName(u"details_frame")
        self.details_frame.setFrameShape(QFrame.StyledPanel)
        self.details_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.details_frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.freq_frame = QFrame(self.details_frame)
        self.freq_frame.setObjectName(u"freq_frame")
        self.freq_frame.setFrameShape(QFrame.StyledPanel)
        self.freq_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.freq_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.freq_group = QGroupBox(self.freq_frame)
        self.freq_group.setObjectName(u"freq_group")
        self.freq_group.setMaximumSize(QSize(200, 16777215))
        self.formLayout_2 = QFormLayout(self.freq_group)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.min_freq_label = QLabel(self.freq_group)
        self.min_freq_label.setObjectName(u"min_freq_label")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.min_freq_label)

        self.min_freq_input = QLineEdit(self.freq_group)
        self.min_freq_input.setObjectName(u"min_freq_input")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.min_freq_input)

        self.max_freq_label = QLabel(self.freq_group)
        self.max_freq_label.setObjectName(u"max_freq_label")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.max_freq_label)

        self.max_freq_input = QLineEdit(self.freq_group)
        self.max_freq_input.setObjectName(u"max_freq_input")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.max_freq_input)

        self.low_freq_label = QLabel(self.freq_group)
        self.low_freq_label.setObjectName(u"low_freq_label")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.low_freq_label)

        self.low_freq_input = QLineEdit(self.freq_group)
        self.low_freq_input.setObjectName(u"low_freq_input")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.low_freq_input)

        self.high_freq_label = QLabel(self.freq_group)
        self.high_freq_label.setObjectName(u"high_freq_label")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.high_freq_label)

        self.high_freq_input = QLineEdit(self.freq_group)
        self.high_freq_input.setObjectName(u"high_freq_input")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.high_freq_input)


        self.horizontalLayout.addWidget(self.freq_group)

        self.voltage_group = QGroupBox(self.freq_frame)
        self.voltage_group.setObjectName(u"voltage_group")
        self.formLayout = QFormLayout(self.voltage_group)
        self.formLayout.setObjectName(u"formLayout")
        self.min_voltage_label = QLabel(self.voltage_group)
        self.min_voltage_label.setObjectName(u"min_voltage_label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.min_voltage_label)

        self.min_voltage_input = QLineEdit(self.voltage_group)
        self.min_voltage_input.setObjectName(u"min_voltage_input")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.min_voltage_input)

        self.max_voltage_label = QLabel(self.voltage_group)
        self.max_voltage_label.setObjectName(u"max_voltage_label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.max_voltage_label)

        self.max_voltage_linput = QLineEdit(self.voltage_group)
        self.max_voltage_linput.setObjectName(u"max_voltage_linput")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.max_voltage_linput)


        self.horizontalLayout.addWidget(self.voltage_group)


        self.verticalLayout_2.addWidget(self.freq_frame)

        self.other_details = QGroupBox(self.details_frame)
        self.other_details.setObjectName(u"other_details")
        self.verticalLayout = QVBoxLayout(self.other_details)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.other_details)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 740, 663))
        self.formLayout_3 = QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.blend_factor_label = QLabel(self.scrollAreaWidgetContents)
        self.blend_factor_label.setObjectName(u"blend_factor_label")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.blend_factor_label)

        self.blend_factor_input = QLineEdit(self.scrollAreaWidgetContents)
        self.blend_factor_input.setObjectName(u"blend_factor_input")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.blend_factor_input)

        self.cs_label = QLabel(self.scrollAreaWidgetContents)
        self.cs_label.setObjectName(u"cs_label")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.cs_label)

        self.casuality_strength_input = QLineEdit(self.scrollAreaWidgetContents)
        self.casuality_strength_input.setObjectName(u"casuality_strength_input")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.casuality_strength_input)

        self.centroid_factor_label = QLabel(self.scrollAreaWidgetContents)
        self.centroid_factor_label.setObjectName(u"centroid_factor_label")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.centroid_factor_label)

        self.centroid_factor_input = QLineEdit(self.scrollAreaWidgetContents)
        self.centroid_factor_input.setObjectName(u"centroid_factor_input")

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.centroid_factor_input)

        self.complex_factor_label = QLabel(self.scrollAreaWidgetContents)
        self.complex_factor_label.setObjectName(u"complex_factor_label")

        self.formLayout_3.setWidget(3, QFormLayout.LabelRole, self.complex_factor_label)

        self.complexity_factor_input = QLineEdit(self.scrollAreaWidgetContents)
        self.complexity_factor_input.setObjectName(u"complexity_factor_input")

        self.formLayout_3.setWidget(3, QFormLayout.FieldRole, self.complexity_factor_input)

        self.edf_label = QLabel(self.scrollAreaWidgetContents)
        self.edf_label.setObjectName(u"edf_label")

        self.formLayout_3.setWidget(4, QFormLayout.LabelRole, self.edf_label)

        self.edge_density_factor = QLineEdit(self.scrollAreaWidgetContents)
        self.edge_density_factor.setObjectName(u"edge_density_factor")

        self.formLayout_3.setWidget(4, QFormLayout.FieldRole, self.edge_density_factor)

        self.er_label = QLabel(self.scrollAreaWidgetContents)
        self.er_label.setObjectName(u"er_label")

        self.formLayout_3.setWidget(5, QFormLayout.LabelRole, self.er_label)

        self.evolution_rate_input = QLineEdit(self.scrollAreaWidgetContents)
        self.evolution_rate_input.setObjectName(u"evolution_rate_input")

        self.formLayout_3.setWidget(5, QFormLayout.FieldRole, self.evolution_rate_input)

        self.fractal_dimes_label = QLabel(self.scrollAreaWidgetContents)
        self.fractal_dimes_label.setObjectName(u"fractal_dimes_label")

        self.formLayout_3.setWidget(6, QFormLayout.LabelRole, self.fractal_dimes_label)

        self.fractal_dimension_input = QLineEdit(self.scrollAreaWidgetContents)
        self.fractal_dimension_input.setObjectName(u"fractal_dimension_input")

        self.formLayout_3.setWidget(6, QFormLayout.FieldRole, self.fractal_dimension_input)

        self.global_sync_label = QLabel(self.scrollAreaWidgetContents)
        self.global_sync_label.setObjectName(u"global_sync_label")

        self.formLayout_3.setWidget(7, QFormLayout.LabelRole, self.global_sync_label)

        self.global_sync_input = QLineEdit(self.scrollAreaWidgetContents)
        self.global_sync_input.setObjectName(u"global_sync_input")

        self.formLayout_3.setWidget(7, QFormLayout.FieldRole, self.global_sync_input)

        self.influence_factor_label = QLabel(self.scrollAreaWidgetContents)
        self.influence_factor_label.setObjectName(u"influence_factor_label")

        self.formLayout_3.setWidget(8, QFormLayout.LabelRole, self.influence_factor_label)

        self.incluence_factor_input = QLineEdit(self.scrollAreaWidgetContents)
        self.incluence_factor_input.setObjectName(u"incluence_factor_input")

        self.formLayout_3.setWidget(8, QFormLayout.FieldRole, self.incluence_factor_input)

        self.max_influence_label = QLabel(self.scrollAreaWidgetContents)
        self.max_influence_label.setObjectName(u"max_influence_label")

        self.formLayout_3.setWidget(9, QFormLayout.LabelRole, self.max_influence_label)

        self.max_influence_label_2 = QLineEdit(self.scrollAreaWidgetContents)
        self.max_influence_label_2.setObjectName(u"max_influence_label_2")

        self.formLayout_3.setWidget(9, QFormLayout.FieldRole, self.max_influence_label_2)

        self.num_imfs_label = QLabel(self.scrollAreaWidgetContents)
        self.num_imfs_label.setObjectName(u"num_imfs_label")

        self.formLayout_3.setWidget(10, QFormLayout.LabelRole, self.num_imfs_label)

        self.num_imfs_input = QLineEdit(self.scrollAreaWidgetContents)
        self.num_imfs_input.setObjectName(u"num_imfs_input")

        self.formLayout_3.setWidget(10, QFormLayout.FieldRole, self.num_imfs_input)

        self.num_peaks_label = QLabel(self.scrollAreaWidgetContents)
        self.num_peaks_label.setObjectName(u"num_peaks_label")

        self.formLayout_3.setWidget(11, QFormLayout.LabelRole, self.num_peaks_label)

        self.num_peak_input = QLineEdit(self.scrollAreaWidgetContents)
        self.num_peak_input.setObjectName(u"num_peak_input")

        self.formLayout_3.setWidget(11, QFormLayout.FieldRole, self.num_peak_input)

        self.sync_level_label = QLabel(self.scrollAreaWidgetContents)
        self.sync_level_label.setObjectName(u"sync_level_label")

        self.formLayout_3.setWidget(12, QFormLayout.LabelRole, self.sync_level_label)

        self.p_sync_input = QLineEdit(self.scrollAreaWidgetContents)
        self.p_sync_input.setObjectName(u"p_sync_input")

        self.formLayout_3.setWidget(12, QFormLayout.FieldRole, self.p_sync_input)

        self.peak_height_label = QLabel(self.scrollAreaWidgetContents)
        self.peak_height_label.setObjectName(u"peak_height_label")

        self.formLayout_3.setWidget(13, QFormLayout.LabelRole, self.peak_height_label)

        self.peak_height_input = QLineEdit(self.scrollAreaWidgetContents)
        self.peak_height_input.setObjectName(u"peak_height_input")

        self.formLayout_3.setWidget(13, QFormLayout.FieldRole, self.peak_height_input)

        self.rms_label = QLabel(self.scrollAreaWidgetContents)
        self.rms_label.setObjectName(u"rms_label")

        self.formLayout_3.setWidget(14, QFormLayout.LabelRole, self.rms_label)

        self.std_dev_label = QLabel(self.scrollAreaWidgetContents)
        self.std_dev_label.setObjectName(u"std_dev_label")

        self.formLayout_3.setWidget(15, QFormLayout.LabelRole, self.std_dev_label)

        self.rms_input = QLineEdit(self.scrollAreaWidgetContents)
        self.rms_input.setObjectName(u"rms_input")

        self.formLayout_3.setWidget(14, QFormLayout.FieldRole, self.rms_input)

        self.std_dev_input = QLineEdit(self.scrollAreaWidgetContents)
        self.std_dev_input.setObjectName(u"std_dev_input")

        self.formLayout_3.setWidget(15, QFormLayout.FieldRole, self.std_dev_input)

        self.sync_factor_label = QLabel(self.scrollAreaWidgetContents)
        self.sync_factor_label.setObjectName(u"sync_factor_label")

        self.formLayout_3.setWidget(16, QFormLayout.LabelRole, self.sync_factor_label)

        self.sync_factor_input = QLineEdit(self.scrollAreaWidgetContents)
        self.sync_factor_input.setObjectName(u"sync_factor_input")

        self.formLayout_3.setWidget(16, QFormLayout.FieldRole, self.sync_factor_input)

        self.target_rate_label = QLabel(self.scrollAreaWidgetContents)
        self.target_rate_label.setObjectName(u"target_rate_label")

        self.formLayout_3.setWidget(17, QFormLayout.LabelRole, self.target_rate_label)

        self.target_rate_input = QLineEdit(self.scrollAreaWidgetContents)
        self.target_rate_input.setObjectName(u"target_rate_input")

        self.formLayout_3.setWidget(17, QFormLayout.FieldRole, self.target_rate_input)

        self.variability_factor_label = QLabel(self.scrollAreaWidgetContents)
        self.variability_factor_label.setObjectName(u"variability_factor_label")

        self.formLayout_3.setWidget(18, QFormLayout.LabelRole, self.variability_factor_label)

        self.var_label = QLabel(self.scrollAreaWidgetContents)
        self.var_label.setObjectName(u"var_label")

        self.formLayout_3.setWidget(19, QFormLayout.LabelRole, self.var_label)

        self.window_size_label = QLabel(self.scrollAreaWidgetContents)
        self.window_size_label.setObjectName(u"window_size_label")

        self.formLayout_3.setWidget(20, QFormLayout.LabelRole, self.window_size_label)

        self.variability_factor_input = QLineEdit(self.scrollAreaWidgetContents)
        self.variability_factor_input.setObjectName(u"variability_factor_input")

        self.formLayout_3.setWidget(18, QFormLayout.FieldRole, self.variability_factor_input)

        self.variance_input = QLineEdit(self.scrollAreaWidgetContents)
        self.variance_input.setObjectName(u"variance_input")

        self.formLayout_3.setWidget(19, QFormLayout.FieldRole, self.variance_input)

        self.window_size_input = QLineEdit(self.scrollAreaWidgetContents)
        self.window_size_input.setObjectName(u"window_size_input")

        self.formLayout_3.setWidget(20, QFormLayout.FieldRole, self.window_size_input)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.verticalLayout_2.addWidget(self.other_details)


        self.verticalLayout_3.addWidget(self.details_frame)
 
        # Simulation Settings Group Box
        self.simulation_settings_group = QGroupBox(self.freq_frame)
        self.simulation_settings_group.setObjectName(u"simulation_settings_group")
        self.simulation_settings_group.setTitle(QCoreApplication.translate("MainWindow", u"Simulation Settings", None))
        self.simulation_formLayout = QFormLayout(self.simulation_settings_group)
        
        # Bit Depth Input
        self.bit_depth_label = QLabel(self.simulation_settings_group)
        self.bit_depth_label.setObjectName(u"bit_depth_label")
        self.bit_depth_label.setText(QCoreApplication.translate("MainWindow", u"Bit Depth:", None))
        self.bit_depth_input = QLineEdit(self.simulation_settings_group)
        self.bit_depth_input.setObjectName(u"bit_depth_input")
        self.simulation_formLayout.addRow(self.bit_depth_label, self.bit_depth_input)
        self.bit_depth_input.textChanged.connect(self.updateBitDepth)

        # Num Signals Input
        self.num_signals_label = QLabel(self.simulation_settings_group)
        self.num_signals_label.setObjectName(u"num_signals_label")
        self.num_signals_label.setText(QCoreApplication.translate("MainWindow", u"Num Signals:", None))
        self.num_signals_input = QLineEdit(self.simulation_settings_group)
        self.num_signals_input.setObjectName(u"num_signals_input")
        self.simulation_formLayout.addRow(self.num_signals_label, self.num_signals_input)
        self.bit_depth_input.textChanged.connect(self.updatenNumSignals)

        # Sampling Frequency Input
        self.fs_label = QLabel(self.simulation_settings_group)
        self.fs_label.setObjectName(u"fs_label")
        self.fs_label.setText(QCoreApplication.translate("MainWindow", u"Sampling Frequency (Hz):", None))
        self.fs_input = QLineEdit(self.simulation_settings_group)
        self.fs_input.setObjectName(u"fs_input")
        self.simulation_formLayout.addRow(self.fs_label, self.fs_input)
        
        # Duration Input
        self.duration_label = QLabel(self.simulation_settings_group)
        self.duration_label.setObjectName(u"duration_label")
        self.duration_label.setText(QCoreApplication.translate("MainWindow", u"Duration (s):", None))
        self.duration_input = QLineEdit(self.simulation_settings_group)
        self.duration_input.setObjectName(u"duration_input")
        self.simulation_formLayout.addRow(self.duration_label, self.duration_input)
        
        # Min Volt Input
        self.min_volt_label = QLabel(self.simulation_settings_group)
        self.min_volt_label.setObjectName(u"min_volt_label")
        self.min_volt_label.setText(QCoreApplication.translate("MainWindow", u"Min Volt (V):", None))
        self.min_volt_input = QLineEdit(self.simulation_settings_group)
        self.min_volt_input.setObjectName(u"min_volt_input")
        self.simulation_formLayout.addRow(self.min_volt_label, self.min_volt_input)
        
        # Max Volt Input
        self.max_volt_label = QLabel(self.simulation_settings_group)
        self.max_volt_label.setObjectName(u"max_volt_label")
        self.max_volt_label.setText(QCoreApplication.translate("MainWindow", u"Max Volt (V):", None))
        self.max_volt_input = QLineEdit(self.simulation_settings_group)
        self.max_volt_input.setObjectName(u"max_volt_input")
        self.simulation_formLayout.addRow(self.max_volt_label, self.max_volt_input)
        
        # Add the Simulation Settings Group Box to the layout
        self.horizontalLayout.addWidget(self.simulation_settings_group)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 800, 22))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menuBar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionLoad_Config)
        self.menuFile.addAction(self.actionSave_Config)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionChange_Export_Path)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionParameters)
        self.menuHelp.addAction(self.actionGitHub)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionLoad_Config.setText(QCoreApplication.translate("MainWindow", u"Load Config", None))
#if QT_CONFIG(shortcut)
        self.actionLoad_Config.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+L", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_Config.setText(QCoreApplication.translate("MainWindow", u"Save Config", None))
#if QT_CONFIG(shortcut)
        self.actionSave_Config.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionChange_Export_Path.setText(QCoreApplication.translate("MainWindow", u"Change Export Path", None))
#if QT_CONFIG(shortcut)
        self.actionChange_Export_Path.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+F", None))
#endif // QT_CONFIG(shortcut)
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionParameters.setText(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.actionGitHub.setText(QCoreApplication.translate("MainWindow", u"GitHub", None))
        self.actionsave_values.setText(QCoreApplication.translate("MainWindow", u"save_values", None))
#if QT_CONFIG(tooltip)
        self.actionsave_values.setToolTip(QCoreApplication.translate("MainWindow", u"Save Values", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionsave_values.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+U", None))
#endif // QT_CONFIG(shortcut)
        self.simulate_btn.setText(QCoreApplication.translate("MainWindow", u"Simulate", None))
        self.clear_all_btn.setText(QCoreApplication.translate("MainWindow", u"Clear All", None))
        self.freq_group.setTitle(QCoreApplication.translate("MainWindow", u"Frequency (Hz)", None))
        self.min_freq_label.setText(QCoreApplication.translate("MainWindow", u"Min: ", None))
        self.max_freq_label.setText(QCoreApplication.translate("MainWindow", u"Max: ", None))
        self.low_freq_label.setText(QCoreApplication.translate("MainWindow", u"Low: ", None))
        self.high_freq_label.setText(QCoreApplication.translate("MainWindow", u"High: ", None))
        self.voltage_group.setTitle(QCoreApplication.translate("MainWindow", u"Voltage (mV)", None))
        self.min_voltage_label.setText(QCoreApplication.translate("MainWindow", u"Min: ", None))
        self.max_voltage_label.setText(QCoreApplication.translate("MainWindow", u"Max: ", None))
        self.other_details.setTitle(QCoreApplication.translate("MainWindow", u"Others:", None))
        self.blend_factor_label.setText(QCoreApplication.translate("MainWindow", u"Blend Factor: ", None))
        self.cs_label.setText(QCoreApplication.translate("MainWindow", u"Casuality Strength: ", None))
        self.centroid_factor_label.setText(QCoreApplication.translate("MainWindow", u"Centroid Factor: ", None))
        self.complex_factor_label.setText(QCoreApplication.translate("MainWindow", u"Complexity Factor: ", None))
        self.edf_label.setText(QCoreApplication.translate("MainWindow", u"Edge Density Factor: ", None))
        self.er_label.setText(QCoreApplication.translate("MainWindow", u"Evolution Rate: ", None))
        self.fractal_dimes_label.setText(QCoreApplication.translate("MainWindow", u"Fractal Dimension: ", None))
        self.global_sync_label.setText(QCoreApplication.translate("MainWindow", u"Global Sync Level: ", None))
        self.influence_factor_label.setText(QCoreApplication.translate("MainWindow", u"Influence Factor:", None))
        self.max_influence_label.setText(QCoreApplication.translate("MainWindow", u"Max Influence: ", None))
        self.num_imfs_label.setText(QCoreApplication.translate("MainWindow", u"Num Imfs: ", None))
        self.num_peaks_label.setText(QCoreApplication.translate("MainWindow", u"Num Peaks: ", None))
        self.sync_level_label.setText(QCoreApplication.translate("MainWindow", u"Pairwise Sync Level: ", None))
        self.peak_height_label.setText(QCoreApplication.translate("MainWindow", u"Peak Height: ", None))
        self.rms_label.setText(QCoreApplication.translate("MainWindow", u"RMS Value: ", None))
        self.std_dev_label.setText(QCoreApplication.translate("MainWindow", u"Standard Deviation: ", None))
        self.sync_factor_label.setText(QCoreApplication.translate("MainWindow", u"Sync Factor: ", None))
        self.target_rate_label.setText(QCoreApplication.translate("MainWindow", u"Target Rate: ", None))
        self.variability_factor_label.setText(QCoreApplication.translate("MainWindow", u"Variability Factor: ", None))
        self.var_label.setText(QCoreApplication.translate("MainWindow", u"Variance: ", None))
        self.window_size_label.setText(QCoreApplication.translate("MainWindow", u"Window Size: ", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

