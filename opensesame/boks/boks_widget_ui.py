# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'boks_widget.ui'
#
# Created: Sun Mar  3 18:33:22 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_boks_widget(object):
    def setupUi(self, boks_widget):
        boks_widget.setObjectName(_fromUtf8("boks_widget"))
        boks_widget.resize(855, 737)
        self.gridLayout = QtGui.QGridLayout(boks_widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        self.frame_controls = QtGui.QFrame(boks_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_controls.sizePolicy().hasHeightForWidth())
        self.frame_controls.setSizePolicy(sizePolicy)
        self.frame_controls.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_controls.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_controls.setObjectName(_fromUtf8("frame_controls"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame_controls)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.edit_dev = QtGui.QLineEdit(self.frame_controls)
        self.edit_dev.setObjectName(_fromUtf8("edit_dev"))
        self.gridLayout_3.addWidget(self.edit_dev, 1, 1, 1, 1)
        self.button_start_test = QtGui.QPushButton(self.frame_controls)
        self.button_start_test.setObjectName(_fromUtf8("button_start_test"))
        self.gridLayout_3.addWidget(self.button_start_test, 6, 0, 1, 2)
        self.label_timeout = QtGui.QLabel(self.frame_controls)
        self.label_timeout.setObjectName(_fromUtf8("label_timeout"))
        self.gridLayout_3.addWidget(self.label_timeout, 5, 0, 1, 1)
        self.edit_correct_response = QtGui.QLineEdit(self.frame_controls)
        self.edit_correct_response.setObjectName(_fromUtf8("edit_correct_response"))
        self.gridLayout_3.addWidget(self.edit_correct_response, 3, 1, 1, 1)
        self.checkbox_dummy = QtGui.QCheckBox(self.frame_controls)
        self.checkbox_dummy.setObjectName(_fromUtf8("checkbox_dummy"))
        self.gridLayout_3.addWidget(self.checkbox_dummy, 2, 0, 1, 2)
        self.edit_allowed_responses = QtGui.QLineEdit(self.frame_controls)
        self.edit_allowed_responses.setText(_fromUtf8(""))
        self.edit_allowed_responses.setObjectName(_fromUtf8("edit_allowed_responses"))
        self.gridLayout_3.addWidget(self.edit_allowed_responses, 4, 1, 1, 1)
        self.label_allowed_responses = QtGui.QLabel(self.frame_controls)
        self.label_allowed_responses.setObjectName(_fromUtf8("label_allowed_responses"))
        self.gridLayout_3.addWidget(self.label_allowed_responses, 4, 0, 1, 1)
        self.label_correct_response = QtGui.QLabel(self.frame_controls)
        self.label_correct_response.setObjectName(_fromUtf8("label_correct_response"))
        self.gridLayout_3.addWidget(self.label_correct_response, 3, 0, 1, 1)
        self.widget = QtGui.QWidget(self.frame_controls)
        self.widget.setStyleSheet(_fromUtf8("background-color: #729fcf;\n"
"color: rgb(255, 255, 255);"))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(5)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_boks_icon = QtGui.QLabel(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_boks_icon.sizePolicy().hasHeightForWidth())
        self.label_boks_icon.setSizePolicy(sizePolicy)
        self.label_boks_icon.setText(_fromUtf8(""))
        self.label_boks_icon.setObjectName(_fromUtf8("label_boks_icon"))
        self.horizontalLayout.addWidget(self.label_boks_icon)
        self.label_boks = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_boks.setFont(font)
        self.label_boks.setObjectName(_fromUtf8("label_boks"))
        self.horizontalLayout.addWidget(self.label_boks)
        self.gridLayout_3.addWidget(self.widget, 0, 0, 1, 3)
        self.widget_test = QtGui.QWidget(self.frame_controls)
        self.widget_test.setObjectName(_fromUtf8("widget_test"))
        self.gridLayout_4 = QtGui.QGridLayout(self.widget_test)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_sid = QtGui.QLabel(self.widget_test)
        self.label_sid.setObjectName(_fromUtf8("label_sid"))
        self.gridLayout_4.addWidget(self.label_sid, 5, 0, 1, 1)
        self.edit_firmware_version = QtGui.QLineEdit(self.widget_test)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monospace"))
        self.edit_firmware_version.setFont(font)
        self.edit_firmware_version.setReadOnly(True)
        self.edit_firmware_version.setObjectName(_fromUtf8("edit_firmware_version"))
        self.gridLayout_4.addWidget(self.edit_firmware_version, 3, 1, 1, 1)
        self.label_model = QtGui.QLabel(self.widget_test)
        self.label_model.setObjectName(_fromUtf8("label_model"))
        self.gridLayout_4.addWidget(self.label_model, 2, 0, 1, 1)
        self.label_firmware_version = QtGui.QLabel(self.widget_test)
        self.label_firmware_version.setObjectName(_fromUtf8("label_firmware_version"))
        self.gridLayout_4.addWidget(self.label_firmware_version, 3, 0, 1, 1)
        self.edit_sid = QtGui.QLineEdit(self.widget_test)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monospace"))
        self.edit_sid.setFont(font)
        self.edit_sid.setReadOnly(True)
        self.edit_sid.setObjectName(_fromUtf8("edit_sid"))
        self.gridLayout_4.addWidget(self.edit_sid, 5, 1, 1, 1)
        self.frame = QtGui.QFrame(self.widget_test)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 140))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.button_2 = QtGui.QPushButton(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_2.sizePolicy().hasHeightForWidth())
        self.button_2.setSizePolicy(sizePolicy)
        self.button_2.setText(_fromUtf8(""))
        self.button_2.setIconSize(QtCore.QSize(32, 32))
        self.button_2.setFlat(True)
        self.button_2.setObjectName(_fromUtf8("button_2"))
        self.gridLayout_2.addWidget(self.button_2, 1, 1, 1, 1)
        self.button_4 = QtGui.QPushButton(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_4.sizePolicy().hasHeightForWidth())
        self.button_4.setSizePolicy(sizePolicy)
        self.button_4.setText(_fromUtf8(""))
        self.button_4.setIconSize(QtCore.QSize(32, 32))
        self.button_4.setFlat(True)
        self.button_4.setObjectName(_fromUtf8("button_4"))
        self.gridLayout_2.addWidget(self.button_4, 1, 3, 1, 1)
        self.button_3 = QtGui.QPushButton(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_3.sizePolicy().hasHeightForWidth())
        self.button_3.setSizePolicy(sizePolicy)
        self.button_3.setText(_fromUtf8(""))
        self.button_3.setIconSize(QtCore.QSize(32, 32))
        self.button_3.setFlat(True)
        self.button_3.setObjectName(_fromUtf8("button_3"))
        self.gridLayout_2.addWidget(self.button_3, 1, 2, 1, 1)
        self.label_boks_test = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_boks_test.sizePolicy().hasHeightForWidth())
        self.label_boks_test.setSizePolicy(sizePolicy)
        self.label_boks_test.setWordWrap(True)
        self.label_boks_test.setObjectName(_fromUtf8("label_boks_test"))
        self.gridLayout_2.addWidget(self.label_boks_test, 0, 0, 1, 5)
        self.button_1 = QtGui.QPushButton(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_1.sizePolicy().hasHeightForWidth())
        self.button_1.setSizePolicy(sizePolicy)
        self.button_1.setText(_fromUtf8(""))
        self.button_1.setIconSize(QtCore.QSize(32, 32))
        self.button_1.setFlat(True)
        self.button_1.setObjectName(_fromUtf8("button_1"))
        self.gridLayout_2.addWidget(self.button_1, 1, 0, 1, 1)
        self.button_5 = QtGui.QPushButton(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_5.sizePolicy().hasHeightForWidth())
        self.button_5.setSizePolicy(sizePolicy)
        self.button_5.setText(_fromUtf8(""))
        self.button_5.setIconSize(QtCore.QSize(32, 32))
        self.button_5.setFlat(True)
        self.button_5.setObjectName(_fromUtf8("button_5"))
        self.gridLayout_2.addWidget(self.button_5, 2, 0, 1, 1)
        self.button_6 = QtGui.QPushButton(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_6.sizePolicy().hasHeightForWidth())
        self.button_6.setSizePolicy(sizePolicy)
        self.button_6.setText(_fromUtf8(""))
        self.button_6.setIconSize(QtCore.QSize(32, 32))
        self.button_6.setFlat(True)
        self.button_6.setObjectName(_fromUtf8("button_6"))
        self.gridLayout_2.addWidget(self.button_6, 2, 1, 1, 1)
        self.button_7 = QtGui.QPushButton(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_7.sizePolicy().hasHeightForWidth())
        self.button_7.setSizePolicy(sizePolicy)
        self.button_7.setText(_fromUtf8(""))
        self.button_7.setIconSize(QtCore.QSize(32, 32))
        self.button_7.setFlat(True)
        self.button_7.setObjectName(_fromUtf8("button_7"))
        self.gridLayout_2.addWidget(self.button_7, 2, 2, 1, 1)
        self.button_8 = QtGui.QPushButton(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_8.sizePolicy().hasHeightForWidth())
        self.button_8.setSizePolicy(sizePolicy)
        self.button_8.setText(_fromUtf8(""))
        self.button_8.setIconSize(QtCore.QSize(32, 32))
        self.button_8.setFlat(True)
        self.button_8.setObjectName(_fromUtf8("button_8"))
        self.gridLayout_2.addWidget(self.button_8, 2, 3, 1, 1)
        self.gridLayout_4.addWidget(self.frame, 1, 0, 1, 2)
        self.button_stop_test = QtGui.QPushButton(self.widget_test)
        self.button_stop_test.setObjectName(_fromUtf8("button_stop_test"))
        self.gridLayout_4.addWidget(self.button_stop_test, 0, 0, 1, 2)
        self.label_button_count = QtGui.QLabel(self.widget_test)
        self.label_button_count.setObjectName(_fromUtf8("label_button_count"))
        self.gridLayout_4.addWidget(self.label_button_count, 4, 0, 1, 1)
        self.spinbox_button_count = QtGui.QSpinBox(self.widget_test)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monospace"))
        self.spinbox_button_count.setFont(font)
        self.spinbox_button_count.setReadOnly(True)
        self.spinbox_button_count.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.spinbox_button_count.setObjectName(_fromUtf8("spinbox_button_count"))
        self.gridLayout_4.addWidget(self.spinbox_button_count, 4, 1, 1, 1)
        self.edit_model = QtGui.QLineEdit(self.widget_test)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monospace"))
        self.edit_model.setFont(font)
        self.edit_model.setReadOnly(True)
        self.edit_model.setObjectName(_fromUtf8("edit_model"))
        self.gridLayout_4.addWidget(self.edit_model, 2, 1, 1, 1)
        self.gridLayout_3.addWidget(self.widget_test, 8, 0, 1, 2)
        self.edit_timeout = QtGui.QLineEdit(self.frame_controls)
        self.edit_timeout.setObjectName(_fromUtf8("edit_timeout"))
        self.gridLayout_3.addWidget(self.edit_timeout, 5, 1, 1, 1)
        self.label_dev = QtGui.QLabel(self.frame_controls)
        self.label_dev.setObjectName(_fromUtf8("label_dev"))
        self.gridLayout_3.addWidget(self.label_dev, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_controls, 0, 1, 1, 1)

        self.retranslateUi(boks_widget)
        QtCore.QMetaObject.connectSlotsByName(boks_widget)

    def retranslateUi(self, boks_widget):
        boks_widget.setWindowTitle(QtGui.QApplication.translate("boks_widget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_dev.setToolTip(QtGui.QApplication.translate("boks_widget", "The frequence of the sound. Expecting a numeric value (frequency in Hertz) a note (like \'C#2\' and \'A1\') or a variable (like \'[freq]\')", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_dev.setText(QtGui.QApplication.translate("boks_widget", "autodetect", None, QtGui.QApplication.UnicodeUTF8))
        self.button_start_test.setText(QtGui.QApplication.translate("boks_widget", "Start test", None, QtGui.QApplication.UnicodeUTF8))
        self.label_timeout.setText(QtGui.QApplication.translate("boks_widget", "Timeout", None, QtGui.QApplication.UnicodeUTF8))
        self.checkbox_dummy.setText(QtGui.QApplication.translate("boks_widget", "Dummy mode (use keyboard instead)", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_allowed_responses.setToolTip(QtGui.QApplication.translate("boks_widget", "Set the duration of the synth item. Expecting a duration in ms, \'sound\' (to wait until the sound is finished playing), \'keypress\', \'mouseclick\', or a variable (e.g., \'[synth_dur]\').", None, QtGui.QApplication.UnicodeUTF8))
        self.label_allowed_responses.setText(QtGui.QApplication.translate("boks_widget", "Allowed responses", None, QtGui.QApplication.UnicodeUTF8))
        self.label_correct_response.setText(QtGui.QApplication.translate("boks_widget", "Correct response", None, QtGui.QApplication.UnicodeUTF8))
        self.label_boks.setText(QtGui.QApplication.translate("boks_widget", "Boks plug-in v%s", None, QtGui.QApplication.UnicodeUTF8))
        self.label_sid.setText(QtGui.QApplication.translate("boks_widget", "Serial ID", None, QtGui.QApplication.UnicodeUTF8))
        self.label_model.setText(QtGui.QApplication.translate("boks_widget", "Model", None, QtGui.QApplication.UnicodeUTF8))
        self.label_firmware_version.setText(QtGui.QApplication.translate("boks_widget", "Firmware version", None, QtGui.QApplication.UnicodeUTF8))
        self.label_boks_test.setText(QtGui.QApplication.translate("boks_widget", "Press the buttons on your boks and see if the buttons below respond. Please stop the test before running the experiment.", None, QtGui.QApplication.UnicodeUTF8))
        self.button_stop_test.setText(QtGui.QApplication.translate("boks_widget", "Stop test", None, QtGui.QApplication.UnicodeUTF8))
        self.label_button_count.setText(QtGui.QApplication.translate("boks_widget", "Nr. of buttons", None, QtGui.QApplication.UnicodeUTF8))
        self.label_dev.setText(QtGui.QApplication.translate("boks_widget", "Device", None, QtGui.QApplication.UnicodeUTF8))

