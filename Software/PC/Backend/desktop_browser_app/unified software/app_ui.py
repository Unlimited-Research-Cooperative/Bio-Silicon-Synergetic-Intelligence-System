# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QMainWindow,
    QPlainTextEdit, QProgressBar, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QToolButton, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.settingsBtn = QToolButton(self.centralwidget)
        self.settingsBtn.setObjectName(u"settingsBtn")
        self.settingsBtn.setMinimumSize(QSize(40, 40))
        icon = QIcon(QIcon.fromTheme(u"preferences-desktop"))
        self.settingsBtn.setIcon(icon)
        self.settingsBtn.setIconSize(QSize(24, 24))

        self.verticalLayout.addWidget(self.settingsBtn, 0, Qt.AlignmentFlag.AlignRight)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout = QGridLayout(self.tab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.dataExportBtn = QPushButton(self.tab)
        self.dataExportBtn.setObjectName(u"dataExportBtn")
        self.dataExportBtn.setMinimumSize(QSize(150, 35))
        self.dataExportBtn.setMaximumSize(QSize(150, 35))
        icon1 = QIcon(QIcon.fromTheme(u"emblem-symbolic-link"))
        self.dataExportBtn.setIcon(icon1)
        self.dataExportBtn.setIconSize(QSize(24, 24))

        self.gridLayout.addWidget(self.dataExportBtn, 1, 1, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.gameActGbox = QGroupBox(self.tab)
        self.gameActGbox.setObjectName(u"gameActGbox")
        self.verticalLayout_3 = QVBoxLayout(self.gameActGbox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gameActEdit = QPlainTextEdit(self.gameActGbox)
        self.gameActEdit.setObjectName(u"gameActEdit")
        self.gameActEdit.setReadOnly(True)

        self.verticalLayout_3.addWidget(self.gameActEdit)


        self.gridLayout.addWidget(self.gameActGbox, 0, 1, 1, 1)

        self.extFeaturesGBox = QGroupBox(self.tab)
        self.extFeaturesGBox.setObjectName(u"extFeaturesGBox")
        self.extFeaturesGBox.setMinimumSize(QSize(300, 0))
        self.verticalLayout_2 = QVBoxLayout(self.extFeaturesGBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 9, 0, 0)
        self.extFeaturesLayout = QFormLayout()
        self.extFeaturesLayout.setObjectName(u"extFeaturesLayout")
        self.extFeaturesLayout.setContentsMargins(-1, 0, -1, -1)

        self.verticalLayout_2.addLayout(self.extFeaturesLayout)


        self.gridLayout.addWidget(self.extFeaturesGBox, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout = QHBoxLayout(self.tab_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.replace_with_video_widget = QFrame(self.tab_2)
        self.replace_with_video_widget.setObjectName(u"replace_with_video_widget")
        self.replace_with_video_widget.setFrameShape(QFrame.Shape.StyledPanel)
        self.replace_with_video_widget.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout.addWidget(self.replace_with_video_widget)

        self.groupBox = QGroupBox(self.tab_2)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(300, 0))
        self.groupBox.setMaximumSize(QSize(300, 16777215))
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.frame = QFrame(self.groupBox)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.formLayout = QFormLayout(self.frame)
        self.formLayout.setObjectName(u"formLayout")
        self.stressMeterLabel = QLabel(self.frame)
        self.stressMeterLabel.setObjectName(u"stressMeterLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.stressMeterLabel)

        self.stressMeter = QProgressBar(self.frame)
        self.stressMeter.setObjectName(u"stressMeter")
        self.stressMeter.setValue(24)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.stressMeter)

        self.scoreLabel = QLabel(self.frame)
        self.scoreLabel.setObjectName(u"scoreLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.scoreLabel)

        self.scoreCount = QLabel(self.frame)
        self.scoreCount.setObjectName(u"scoreCount")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.scoreCount)

        self.relayStatusLabel = QLabel(self.frame)
        self.relayStatusLabel.setObjectName(u"relayStatusLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.relayStatusLabel)

        self.relayStatus = QLabel(self.frame)
        self.relayStatus.setObjectName(u"relayStatus")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.relayStatus)


        self.verticalLayout_4.addWidget(self.frame)

        self.push_reward_btn = QPushButton(self.groupBox)
        self.push_reward_btn.setObjectName(u"push_reward_btn")
        self.push_reward_btn.setMinimumSize(QSize(150, 35))
        self.push_reward_btn.setMaximumSize(QSize(150, 35))
        icon2 = QIcon(QIcon.fromTheme(u"face-smile-big"))
        self.push_reward_btn.setIcon(icon2)
        self.push_reward_btn.setIconSize(QSize(24, 24))

        self.verticalLayout_4.addWidget(self.push_reward_btn, 0, Qt.AlignmentFlag.AlignHCenter)


        self.horizontalLayout.addWidget(self.groupBox)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"BSISS Unified Software", None))
        self.settingsBtn.setText("")
        self.dataExportBtn.setText(QCoreApplication.translate("MainWindow", u"Export Data", None))
        self.gameActGbox.setTitle(QCoreApplication.translate("MainWindow", u"Game Actions", None))
        self.extFeaturesGBox.setTitle(QCoreApplication.translate("MainWindow", u"Extracted Features", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Data Monitor", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Controls", None))
        self.stressMeterLabel.setText(QCoreApplication.translate("MainWindow", u"Stress Meter: ", None))
        self.scoreLabel.setText(QCoreApplication.translate("MainWindow", u"Score: ", None))
        self.scoreCount.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.relayStatusLabel.setText(QCoreApplication.translate("MainWindow", u"Relay Status: ", None))
        self.relayStatus.setText(QCoreApplication.translate("MainWindow", u"Closed", None))
        self.push_reward_btn.setText(QCoreApplication.translate("MainWindow", u"Push Reward", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Game and Reward System", None))
    # retranslateUi

