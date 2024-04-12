# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPlainTextEdit, QPushButton, QSizePolicy, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_SignalsTranslatorWindow(object):
    def setupUi(self, SignalsTranslatorWindow):
        if not SignalsTranslatorWindow.objectName():
            SignalsTranslatorWindow.setObjectName(u"SignalsTranslatorWindow")
        SignalsTranslatorWindow.resize(340, 561)
        SignalsTranslatorWindow.setMaximumSize(QSize(340, 16777215))
        self.centralwidget = QWidget(SignalsTranslatorWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.home_tab = QWidget()
        self.home_tab.setObjectName(u"home_tab")
        self.verticalLayout_2 = QVBoxLayout(self.home_tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(self.home_tab)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 150))
        self.groupBox.setMaximumSize(QSize(16777215, 150))
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(20)
        self.formLayout.setVerticalSpacing(10)
        self.formLayout.setContentsMargins(-1, 10, -1, -1)
        self.hostLabel = QLabel(self.groupBox)
        self.hostLabel.setObjectName(u"hostLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.hostLabel)

        self.hostLineEdit = QLineEdit(self.groupBox)
        self.hostLineEdit.setObjectName(u"hostLineEdit")
        self.hostLineEdit.setEnabled(False)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.hostLineEdit)

        self.portLabel = QLabel(self.groupBox)
        self.portLabel.setObjectName(u"portLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.portLabel)

        self.portLineEdit = QLineEdit(self.groupBox)
        self.portLineEdit.setObjectName(u"portLineEdit")
        self.portLineEdit.setEnabled(False)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.portLineEdit)


        self.verticalLayout_3.addLayout(self.formLayout)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.label = QLabel(self.home_tab)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 30))
        self.label.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout_2.addWidget(self.label)

        self.translatedOutput = QPlainTextEdit(self.home_tab)
        self.translatedOutput.setObjectName(u"translatedOutput")
        self.translatedOutput.setEnabled(False)
        self.translatedOutput.setMinimumSize(QSize(0, 300))
        self.translatedOutput.setMaximumSize(QSize(16777215, 300))

        self.verticalLayout_2.addWidget(self.translatedOutput)

        self.tabWidget.addTab(self.home_tab, "")
        self.settings_tab = QWidget()
        self.settings_tab.setObjectName(u"settings_tab")
        self.verticalLayout_4 = QVBoxLayout(self.settings_tab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setHorizontalSpacing(20)
        self.hostLabel_2 = QLabel(self.settings_tab)
        self.hostLabel_2.setObjectName(u"hostLabel_2")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.hostLabel_2)

        self.hostLineEdit_2 = QLineEdit(self.settings_tab)
        self.hostLineEdit_2.setObjectName(u"hostLineEdit_2")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.hostLineEdit_2)

        self.portLabel_2 = QLabel(self.settings_tab)
        self.portLabel_2.setObjectName(u"portLabel_2")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.portLabel_2)

        self.portLineEdit_2 = QLineEdit(self.settings_tab)
        self.portLineEdit_2.setObjectName(u"portLineEdit_2")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.portLineEdit_2)


        self.verticalLayout_4.addLayout(self.formLayout_2)

        self.msg_label = QLabel(self.settings_tab)
        self.msg_label.setObjectName(u"msg_label")
        self.msg_label.setMinimumSize(QSize(300, 0))
        self.msg_label.setMaximumSize(QSize(300, 16777215))
        self.msg_label.setStyleSheet(u"margin-top: 20px")

        self.verticalLayout_4.addWidget(self.msg_label, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.frame = QFrame(self.settings_tab)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 40))
        self.frame.setMaximumSize(QSize(16777215, 40))
        self.frame.setStyleSheet(u"QFrame{\n"
"	border: 0px solid;\n"
"}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.startBtn = QPushButton(self.frame)
        self.startBtn.setObjectName(u"startBtn")
        self.startBtn.setMinimumSize(QSize(100, 30))
        self.startBtn.setMaximumSize(QSize(100, 30))
        icon = QIcon(QIcon.fromTheme(u"media-playback-start"))
        self.startBtn.setIcon(icon)

        self.horizontalLayout.addWidget(self.startBtn)

        self.export_btn = QPushButton(self.frame)
        self.export_btn.setObjectName(u"export_btn")
        self.export_btn.setMinimumSize(QSize(100, 30))
        self.export_btn.setMaximumSize(QSize(100, 30))
        icon1 = QIcon(QIcon.fromTheme(u"emblem-symbolic-link"))
        self.export_btn.setIcon(icon1)

        self.horizontalLayout.addWidget(self.export_btn)


        self.verticalLayout_4.addWidget(self.frame, 0, Qt.AlignRight)

        self.tabWidget.addTab(self.settings_tab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        SignalsTranslatorWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SignalsTranslatorWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(SignalsTranslatorWindow)
    # setupUi

    def retranslateUi(self, SignalsTranslatorWindow):
        SignalsTranslatorWindow.setWindowTitle(QCoreApplication.translate("SignalsTranslatorWindow", u"Signals Translator", None))
        self.groupBox.setTitle(QCoreApplication.translate("SignalsTranslatorWindow", u"Current Configurations:", None))
        self.hostLabel.setText(QCoreApplication.translate("SignalsTranslatorWindow", u"Host:", None))
        self.portLabel.setText(QCoreApplication.translate("SignalsTranslatorWindow", u"Port:", None))
        self.label.setText(QCoreApplication.translate("SignalsTranslatorWindow", u"Incoming Data", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.home_tab), QCoreApplication.translate("SignalsTranslatorWindow", u"Home", None))
        self.hostLabel_2.setText(QCoreApplication.translate("SignalsTranslatorWindow", u"Host: ", None))
        self.portLabel_2.setText(QCoreApplication.translate("SignalsTranslatorWindow", u"Port: ", None))
        self.msg_label.setText(QCoreApplication.translate("SignalsTranslatorWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Make sure that you are running your <span style=\" font-weight:700;\">Mosquitto Broker </span>(locally or cloud) on the host and port you set.</p></body></html>", None))
        self.startBtn.setText(QCoreApplication.translate("SignalsTranslatorWindow", u"Start", None))
        self.export_btn.setText(QCoreApplication.translate("SignalsTranslatorWindow", u"Export ", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings_tab), QCoreApplication.translate("SignalsTranslatorWindow", u"Settings", None))
    # retranslateUi

