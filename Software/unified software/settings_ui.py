# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFormLayout,
    QFrame, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPlainTextEdit, QPushButton, QSizePolicy,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.resize(459, 420)
        SettingsDialog.setMinimumSize(QSize(459, 420))
        self.verticalLayout = QVBoxLayout(SettingsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(SettingsDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.generalTab = QWidget()
        self.generalTab.setObjectName(u"generalTab")
        self.verticalLayout_2 = QVBoxLayout(self.generalTab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(self.generalTab)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.featuresBox = QComboBox(self.frame)
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.addItem("")
        self.featuresBox.setObjectName(u"featuresBox")
        self.featuresBox.setMinimumSize(QSize(0, 30))
        self.featuresBox.setEditable(True)

        self.horizontalLayout.addWidget(self.featuresBox)

        self.addFeatureBtn = QPushButton(self.frame)
        self.addFeatureBtn.setObjectName(u"addFeatureBtn")
        self.addFeatureBtn.setMinimumSize(QSize(0, 30))
        self.addFeatureBtn.setMaximumSize(QSize(100, 30))

        self.horizontalLayout.addWidget(self.addFeatureBtn)


        self.verticalLayout_2.addWidget(self.frame)

        self.currentFeatures = QPlainTextEdit(self.generalTab)
        self.currentFeatures.setObjectName(u"currentFeatures")
        self.currentFeatures.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.currentFeatures)

        self.frame_3 = QFrame(self.generalTab)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 30))
        self.frame_3.setStyleSheet(u"QFrame{\n"
"	border: 0px solid;\n"
"}")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.apply_feature_btn = QPushButton(self.frame_3)
        self.apply_feature_btn.setObjectName(u"apply_feature_btn")
        self.apply_feature_btn.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_2.addWidget(self.apply_feature_btn)

        self.reset_features_btn = QPushButton(self.frame_3)
        self.reset_features_btn.setObjectName(u"reset_features_btn")
        self.reset_features_btn.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_2.addWidget(self.reset_features_btn)


        self.verticalLayout_2.addWidget(self.frame_3, 0, Qt.AlignmentFlag.AlignRight)

        self.tabWidget.addTab(self.generalTab, "")
        self.connTab = QWidget()
        self.connTab.setObjectName(u"connTab")
        self.verticalLayout_5 = QVBoxLayout(self.connTab)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.frame_2 = QFrame(self.connTab)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.hostLabel = QLabel(self.frame_2)
        self.hostLabel.setObjectName(u"hostLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.hostLabel)

        self.hostLineEdit = QLineEdit(self.frame_2)
        self.hostLineEdit.setObjectName(u"hostLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.hostLineEdit)

        self.portLabel = QLabel(self.frame_2)
        self.portLabel.setObjectName(u"portLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.portLabel)

        self.portLineEdit = QLineEdit(self.frame_2)
        self.portLineEdit.setObjectName(u"portLineEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.portLineEdit)


        self.verticalLayout_3.addLayout(self.formLayout)

        self.apply_conn_btn = QPushButton(self.frame_2)
        self.apply_conn_btn.setObjectName(u"apply_conn_btn")
        self.apply_conn_btn.setMinimumSize(QSize(0, 30))

        self.verticalLayout_3.addWidget(self.apply_conn_btn, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout_5.addWidget(self.frame_2)

        self.groupBox = QGroupBox(self.connTab)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.hostLabel_2 = QLabel(self.groupBox)
        self.hostLabel_2.setObjectName(u"hostLabel_2")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.hostLabel_2)

        self.hostManagerInput = QLineEdit(self.groupBox)
        self.hostManagerInput.setObjectName(u"hostManagerInput")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.hostManagerInput)

        self.portLabel_2 = QLabel(self.groupBox)
        self.portLabel_2.setObjectName(u"portLabel_2")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.portLabel_2)

        self.portManagerInput = QLineEdit(self.groupBox)
        self.portManagerInput.setObjectName(u"portManagerInput")
        self.portManagerInput.setCursorMoveStyle(Qt.CursorMoveStyle.LogicalMoveStyle)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.portManagerInput)

        self.subscriptionTopicLabel = QLabel(self.groupBox)
        self.subscriptionTopicLabel.setObjectName(u"subscriptionTopicLabel")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.subscriptionTopicLabel)

        self.subscriptionTopicLineEdit = QLineEdit(self.groupBox)
        self.subscriptionTopicLineEdit.setObjectName(u"subscriptionTopicLineEdit")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.subscriptionTopicLineEdit)

        self.publishingTopicLabel = QLabel(self.groupBox)
        self.publishingTopicLabel.setObjectName(u"publishingTopicLabel")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.publishingTopicLabel)

        self.publishingTopicLineEdit = QLineEdit(self.groupBox)
        self.publishingTopicLineEdit.setObjectName(u"publishingTopicLineEdit")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.publishingTopicLineEdit)

        self.clientNameLabel = QLabel(self.groupBox)
        self.clientNameLabel.setObjectName(u"clientNameLabel")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.clientNameLabel)

        self.clientNameLineEdit = QLineEdit(self.groupBox)
        self.clientNameLineEdit.setObjectName(u"clientNameLineEdit")

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.clientNameLineEdit)


        self.verticalLayout_4.addLayout(self.formLayout_2)

        self.createBtn = QPushButton(self.groupBox)
        self.createBtn.setObjectName(u"createBtn")
        self.createBtn.setMinimumSize(QSize(0, 30))

        self.verticalLayout_4.addWidget(self.createBtn, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout_5.addWidget(self.groupBox)

        self.tabWidget.addTab(self.connTab, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(SettingsDialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"Settings", None))
        self.featuresBox.setItemText(0, QCoreApplication.translate("SettingsDialog", u"--Select-Feature--", None))
        self.featuresBox.setItemText(1, QCoreApplication.translate("SettingsDialog", u"Minimum Frequency", None))
        self.featuresBox.setItemText(2, QCoreApplication.translate("SettingsDialog", u"Maximum Frequency", None))
        self.featuresBox.setItemText(3, QCoreApplication.translate("SettingsDialog", u"Low Frequency", None))
        self.featuresBox.setItemText(4, QCoreApplication.translate("SettingsDialog", u"High Frequency", None))
        self.featuresBox.setItemText(5, QCoreApplication.translate("SettingsDialog", u"Minimum Voltage", None))
        self.featuresBox.setItemText(6, QCoreApplication.translate("SettingsDialog", u"Maximum Voltage", None))
        self.featuresBox.setItemText(7, QCoreApplication.translate("SettingsDialog", u"Blend Factor", None))
        self.featuresBox.setItemText(8, QCoreApplication.translate("SettingsDialog", u"Casuality Strength", None))
        self.featuresBox.setItemText(9, QCoreApplication.translate("SettingsDialog", u"Centroid Factor", None))
        self.featuresBox.setItemText(10, QCoreApplication.translate("SettingsDialog", u"Complexity Factor", None))
        self.featuresBox.setItemText(11, QCoreApplication.translate("SettingsDialog", u"Edge Density Factor", None))
        self.featuresBox.setItemText(12, QCoreApplication.translate("SettingsDialog", u"Evolution Rate", None))
        self.featuresBox.setItemText(13, QCoreApplication.translate("SettingsDialog", u"Fractal Dimension", None))
        self.featuresBox.setItemText(14, QCoreApplication.translate("SettingsDialog", u"Global Sync Level", None))
        self.featuresBox.setItemText(15, QCoreApplication.translate("SettingsDialog", u"Influence Factor", None))
        self.featuresBox.setItemText(16, QCoreApplication.translate("SettingsDialog", u"Maximum Influence", None))
        self.featuresBox.setItemText(17, QCoreApplication.translate("SettingsDialog", u"Number Of IMFS", None))
        self.featuresBox.setItemText(18, QCoreApplication.translate("SettingsDialog", u"Number Of Peaks", None))
        self.featuresBox.setItemText(19, QCoreApplication.translate("SettingsDialog", u"Pairwise Sync Level", None))
        self.featuresBox.setItemText(20, QCoreApplication.translate("SettingsDialog", u"Peak Height", None))
        self.featuresBox.setItemText(21, QCoreApplication.translate("SettingsDialog", u"RMS Value", None))
        self.featuresBox.setItemText(22, QCoreApplication.translate("SettingsDialog", u"Standard Deviation", None))
        self.featuresBox.setItemText(23, QCoreApplication.translate("SettingsDialog", u"Sync Factor", None))
        self.featuresBox.setItemText(24, QCoreApplication.translate("SettingsDialog", u"Target Rate", None))
        self.featuresBox.setItemText(25, QCoreApplication.translate("SettingsDialog", u"Variability Factor", None))
        self.featuresBox.setItemText(26, QCoreApplication.translate("SettingsDialog", u"Variance", None))
        self.featuresBox.setItemText(27, QCoreApplication.translate("SettingsDialog", u"Window Size", None))

        self.addFeatureBtn.setText(QCoreApplication.translate("SettingsDialog", u"Add", None))
        self.currentFeatures.setPlainText(QCoreApplication.translate("SettingsDialog", u"Current Features:", None))
        self.apply_feature_btn.setText(QCoreApplication.translate("SettingsDialog", u"Apply", None))
        self.reset_features_btn.setText(QCoreApplication.translate("SettingsDialog", u"Reset", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generalTab), QCoreApplication.translate("SettingsDialog", u"General", None))
        self.hostLabel.setText(QCoreApplication.translate("SettingsDialog", u"Host: ", None))
        self.portLabel.setText(QCoreApplication.translate("SettingsDialog", u"Port: ", None))
        self.apply_conn_btn.setText(QCoreApplication.translate("SettingsDialog", u"Apply", None))
        self.groupBox.setTitle(QCoreApplication.translate("SettingsDialog", u"Data Manager - Create Profile", None))
        self.hostLabel_2.setText(QCoreApplication.translate("SettingsDialog", u"Host: ", None))
        self.portLabel_2.setText(QCoreApplication.translate("SettingsDialog", u"Port: ", None))
        self.subscriptionTopicLabel.setText(QCoreApplication.translate("SettingsDialog", u"Subscription Topic: ", None))
        self.publishingTopicLabel.setText(QCoreApplication.translate("SettingsDialog", u"Publishing Topic: ", None))
        self.clientNameLabel.setText(QCoreApplication.translate("SettingsDialog", u"Client Name: ", None))
        self.createBtn.setText(QCoreApplication.translate("SettingsDialog", u"Create", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.connTab), QCoreApplication.translate("SettingsDialog", u"Connection", None))
    # retranslateUi

