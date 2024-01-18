# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mail_cloud.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1121, 557)
        MainWindow.setMinimumSize(QtCore.QSize(1121, 557))
        MainWindow.setMaximumSize(QtCore.QSize(1121, 557))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(239, 239, 239))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(239, 239, 239))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(239, 239, 239))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(239, 239, 239))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        MainWindow.setPalette(palette)
        MainWindow.setAnimated(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(90, 85, 1021, 451))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.tableWidget = QtWidgets.QTableWidget(self.frame_2)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 1001, 431))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.pathEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.pathEdit.setEnabled(False)
        self.pathEdit.setGeometry(QtCore.QRect(155, 28, 941, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pathEdit.setFont(font)
        self.pathEdit.setFrame(False)
        self.pathEdit.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.pathEdit.setObjectName("pathEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 30, 47, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 86, 71, 451))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(5, 68, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.create_Folder = QtWidgets.QToolButton(self.frame)
        self.create_Folder.setGeometry(QtCore.QRect(5, 10, 61, 61))
        self.create_Folder.setAutoFillBackground(False)
        self.create_Folder.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pic/add_folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.create_Folder.setIcon(icon)
        self.create_Folder.setIconSize(QtCore.QSize(50, 50))
        self.create_Folder.setAutoRaise(True)
        self.create_Folder.setObjectName("create_Folder")
        self.delete_Folder = QtWidgets.QToolButton(self.frame)
        self.delete_Folder.setGeometry(QtCore.QRect(5, 101, 61, 61))
        self.delete_Folder.setAutoFillBackground(False)
        self.delete_Folder.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("pic/delete_folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_Folder.setIcon(icon1)
        self.delete_Folder.setIconSize(QtCore.QSize(50, 50))
        self.delete_Folder.setAutoRaise(True)
        self.delete_Folder.setObjectName("delete_Folder")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(5, 156, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.uploadFile = QtWidgets.QToolButton(self.frame)
        self.uploadFile.setGeometry(QtCore.QRect(5, 172, 61, 61))
        self.uploadFile.setAutoFillBackground(False)
        self.uploadFile.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("pic/upload.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.uploadFile.setIcon(icon2)
        self.uploadFile.setIconSize(QtCore.QSize(50, 50))
        self.uploadFile.setAutoRaise(True)
        self.uploadFile.setObjectName("uploadFile")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(5, 226, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.downloadFile = QtWidgets.QToolButton(self.frame)
        self.downloadFile.setGeometry(QtCore.QRect(5, 243, 61, 61))
        self.downloadFile.setAutoFillBackground(False)
        self.downloadFile.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("pic/download.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downloadFile.setIcon(icon3)
        self.downloadFile.setIconSize(QtCore.QSize(50, 50))
        self.downloadFile.setAutoRaise(True)
        self.downloadFile.setObjectName("downloadFile")
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setGeometry(QtCore.QRect(5, 297, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setWordWrap(True)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setGeometry(QtCore.QRect(5, 404, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setWordWrap(True)
        self.label_9.setObjectName("label_9")
        self.exitButton = QtWidgets.QToolButton(self.frame)
        self.exitButton.setGeometry(QtCore.QRect(5, 350, 61, 61))
        self.exitButton.setAutoFillBackground(False)
        self.exitButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("pic/exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exitButton.setIcon(icon4)
        self.exitButton.setIconSize(QtCore.QSize(50, 50))
        self.exitButton.setAutoRaise(True)
        self.exitButton.setObjectName("exitButton")
        self.cloud = QtWidgets.QToolButton(self.centralwidget)
        self.cloud.setEnabled(False)
        self.cloud.setGeometry(QtCore.QRect(0, 0, 91, 71))
        self.cloud.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("pic/cloud.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon5.addPixmap(QtGui.QPixmap("pic/cloud.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.cloud.setIcon(icon5)
        self.cloud.setIconSize(QtCore.QSize(500, 500))
        self.cloud.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.cloud.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.cloud.setAutoRaise(True)
        self.cloud.setObjectName("cloud")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CloudMail.Ru"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Содержимое"))
        self.label.setText(_translate("MainWindow", "Путь:"))
        self.label_2.setText(_translate("MainWindow", "Создать папку"))
        self.create_Folder.setToolTip(_translate("MainWindow", "Создать папку"))
        self.delete_Folder.setToolTip(_translate("MainWindow", "Удалить файл или папку"))
        self.label_3.setText(_translate("MainWindow", "Удалить"))
        self.uploadFile.setToolTip(_translate("MainWindow", "Загрузить файл или папку"))
        self.label_4.setText(_translate("MainWindow", "Загрузить"))
        self.downloadFile.setToolTip(_translate("MainWindow", "Скачать файл или папку"))
        self.label_8.setText(_translate("MainWindow", "Скачать"))
        self.label_9.setText(_translate("MainWindow", "Выход"))
        self.exitButton.setToolTip(_translate("MainWindow", "Скачать файл или папку"))
