# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'signals_param.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QFrame, QLabel, QLineEdit,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_signalParams(object):
    def setupUi(self, signalParams):
        if not signalParams.objectName():
            signalParams.setObjectName(u"signalParams")
        signalParams.resize(400, 187)
        self.verticalLayout = QVBoxLayout(signalParams)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(signalParams)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.formLayout = QFormLayout(self.frame)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(20)
        self.num_signal_label = QLabel(self.frame)
        self.num_signal_label.setObjectName(u"num_signal_label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.num_signal_label)

        self.numSignalInput = QLineEdit(self.frame)
        self.numSignalInput.setObjectName(u"numSignalInput")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.numSignalInput)

        self.bit_depth_label = QLabel(self.frame)
        self.bit_depth_label.setObjectName(u"bit_depth_label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.bit_depth_label)

        self.bit_depth_input = QLineEdit(self.frame)
        self.bit_depth_input.setObjectName(u"bit_depth_input")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.bit_depth_input)

        self.fs_label = QLabel(self.frame)
        self.fs_label.setObjectName(u"fs_label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.fs_label)

        self.fs_input = QLineEdit(self.frame)
        self.fs_input.setObjectName(u"fs_input")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.fs_input)

        self.durationLabel = QLabel(self.frame)
        self.durationLabel.setObjectName(u"durationLabel")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.durationLabel)

        self.durationLineEdit = QLineEdit(self.frame)
        self.durationLineEdit.setObjectName(u"durationLineEdit")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.durationLineEdit)


        self.verticalLayout.addWidget(self.frame)

        self.buttonBox = QDialogButtonBox(signalParams)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(signalParams)
        self.buttonBox.accepted.connect(signalParams.accept)
        self.buttonBox.rejected.connect(signalParams.reject)

        QMetaObject.connectSlotsByName(signalParams)
    # setupUi

    def retranslateUi(self, signalParams):
        signalParams.setWindowTitle(QCoreApplication.translate("signalParams", u"Signals Parameters", None))
        self.num_signal_label.setText(QCoreApplication.translate("signalParams", u"Number Of Signals: ", None))
        self.bit_depth_label.setText(QCoreApplication.translate("signalParams", u"Bit Depth:", None))
        self.fs_label.setText(QCoreApplication.translate("signalParams", u"Sampling Freq: ", None))
        self.durationLabel.setText(QCoreApplication.translate("signalParams", u"Duration", None))
    # retranslateUi

