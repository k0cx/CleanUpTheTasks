"""
Приложение для работы с облаком. Требует для работы следующие библиотеки:
pip install PyQt5 pyqt5-tools wmi cryptocode
"""
import sys
from platform import system as psys
from sys import exit as ext, argv
from pathlib import Path

from cryptocode import encrypt
from PyQt5.QtWidgets import QMessageBox, QAction, QDialog, QLineEdit, QDialogButtonBox, QFormLayout, QInputDialog

from mail_cloud import *
from mail_tools import connect_cloud_folder, create_cloud_folder, delete_cloud_folder, check_setting, authorize
from mail_tools import upload_cloud_file, download_cloud_file, move_cloud_object, copy_cloud_object


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        """
        Инициализация окна приложения, а также дополнительных
        переменных для работы скрипта.
        """
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.create_actions()
        self.create_context_menu()
        self.connect_action()

        self.files = dict()
        self.cut_object = None
        self.copy_object = None
        self.client = None

        self.ui.tableWidget.cellDoubleClicked.connect(self.folder_view)
        self.ui.create_Folder.clicked.connect(self.create_folder)
        self.ui.delete_Folder.clicked.connect(self.delete_folder)
        self.ui.uploadFile.clicked.connect(self.upload_file)
        self.ui.downloadFile.clicked.connect(self.download_file)
        self.ui.exitButton.clicked.connect(self.exit_application)
        self.ui.tableWidget.customContextMenuRequested[QtCore.QPoint].connect(self.create_actions)

    # context menu begin
    def create_actions(self):
        """
        Создание пунктов меню.
        """
        self.copyAction = QAction("&Copy", self)
        self.cutAction = QAction("C&ut", self)
        self.pasteAction = QAction("&Paste", self)
        self.separator = QAction(self)
        self.separator.setSeparator(True)

    def create_context_menu(self):
        """
        Создание контекстного меню.
        """
        self.ui.tableWidget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.ActionsContextMenu)
        self.ui.tableWidget.addAction(self.copyAction)
        self.ui.tableWidget.addAction(self.cutAction)
        self.ui.tableWidget.addAction(self.separator)
        self.ui.tableWidget.addAction(self.pasteAction)

    def connect_action(self):
        """
        Создание действий при выборе пунктов меню.
        """
        self.copyAction.triggered.connect(self.copy_content)
        self.pasteAction.triggered.connect(self.paste_content)
        self.cutAction.triggered.connect(self.cut_content)

    def cut_content(self):
        """
        Действие выполняющееся при выборе пункта "Вырезать"
        """
        self.copy_object = None
        row = self.ui.tableWidget.currentRow()
        text = self.ui.tableWidget.item(row, 0).text()
        self.cut_object = self.files.get(text).get("path")

    def copy_content(self):
        """
        Действие выполняющееся при выборе пункта "Копировать"
        """
        self.cut_object = None
        row = self.ui.tableWidget.currentRow()
        text = self.ui.tableWidget.item(row, 0).text()
        self.copy_object = self.files.get(text).get("path")

    def get_paste_object(self, cc_object: str) -> str:
        """
        Получение пути к объекту копирования - перемещения.
        """
        if self.ui.pathEdit.text().split("/")[-1]:
            paste_object = f'{self.ui.pathEdit.text()}/{cc_object.split("/")[-1]}'
        else:
            paste_object = f'{self.ui.pathEdit.text()}{cc_object.split("/")[-1]}'
        return paste_object

    def paste_content(self):
        """
        Обработка действия при выборе пункта меню "Вставить".
        В зависимости от того, в какой переменной содержаться данные.
        """
        if self.cut_object:
            paste_object = self.get_paste_object(self.cut_object)
            move_cloud_object(self.client, self.cut_object, paste_object)
            self.connect_cloud(self.ui.pathEdit.text().split("/")[-1])
            self.cut_object = None
        if self.copy_object:
            paste_object = self.get_paste_object(self.copy_object)
            copy_cloud_object(self.client, self.copy_object, paste_object)
            self.connect_cloud(self.ui.pathEdit.text().split("/")[-1])
            self.copy_object = None
    # context menu end

    @staticmethod
    def exit_application():
        """
        Завершение работы приложения.
        """
        QtWidgets.QApplication.quit()

    def download_file(self):
        """
        Обработка нажатия на кнопку Скачать.
        """
        row = self.ui.tableWidget.currentRow()
        text = self.ui.tableWidget.item(row, 0).text()
        if text != "...":
            directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Selecting a folder to save in", ".")
            local_path = Path(directory) / text
            if self.ui.pathEdit.text().split("/")[-1]:
                remote_path = f'{self.ui.pathEdit.text()}/{text}'
            else:
                remote_path = f'/{text}'
            if download_cloud_file(self.client, remote_path, local_path):
                QMessageBox.warning(self, "Сообщение", "Загрузка завершена")

    def upload_file(self):
        """
        Обработка нажатия на клавишу Загрузить.
        """
        files = self.getOpenFilesAndDirs(None, "Выбор файла", "", "*.* (*.*)")
        if files:
            for fil in files:
                if self.ui.pathEdit.text().split("/")[-1]:
                    remote_path = f'{self.ui.pathEdit.text()}/{Path(str(fil)).name}'
                    path = self.ui.pathEdit.text().split("/")[-1]
                else:
                    remote_path = f'{self.ui.pathEdit.text()}{Path(str(fil)).name}'
                    path = "..."
                upload_cloud_file(self.client, remote_path, fil)
                self.connect_cloud(path)
            QMessageBox.warning(self, "Сообщение", "Выгрузка завершена")

    def delete_folder(self):
        """
        Обработка нажатия на кнопку Удалить.
        """
        try:
            row = self.ui.tableWidget.currentRow()
            text = self.ui.tableWidget.item(row, 0).text()
            path = self.files.get(text).get("path")
            delete_cloud_folder(self.client, path)
            if self.ui.pathEdit.text().split("/")[-1]:
                self.connect_cloud(self.ui.pathEdit.text().split("/")[-1])
            else:
                self.connect_cloud("...")
            self.files.pop(text)
        except AttributeError:
            pass

    def create_folder(self):
        """
        Обработка нажатия на кнопку "Создать папку".
        """
        folder = self.ui.pathEdit.text()
        input_name, tr = QtWidgets.QInputDialog.getText(self, 'Создать папку', 'Введите имя папки:')
        if tr:
            if folder == "/":
                name = f'/{input_name}'
            else:
                name = "/".join([folder, input_name])
            if create_cloud_folder(self.client, name):
                self.files.update({input_name: {"path": f'{name}', "isdir": True}})
                self.connect_cloud(input_name)
        else:
            pass

    def folder_view(self):
        """
        Обработка двойного клика в таблице приложения.
        """
        row = self.ui.tableWidget.currentRow()
        text = self.ui.tableWidget.item(row, 0).text()
        if self.files.get(text).get("isdir"):
            self.connect_cloud(text)
        else:
            download_cloud_file(self.client, self.files.get(text).get("path"), str(Path.cwd() / text))
            QMessageBox.warning(self, "Сообщение", "Загрузка завершена в текущую директорию")

    def connect_cloud(self, path: str):
        """
        Получение словаря с данными о папках и файлах в выбранной директории облака.
        """
        if self.files:
            self.ui.pathEdit.setText(self.files.get(path).get("path"))
            files = connect_cloud_folder(self.client, self.files.get(path).get("path"))
            path = "/".join(self.files.get(path).get("path").split("/")[:-1])
            if path:
                self.table_construct(files, path)
            else:
                self.table_construct(files, "/")
        else:
            self.ui.pathEdit.setText(path)
            files = connect_cloud_folder(self.client, path)
            self.table_construct(files, path)

    def table_construct(self, files: list, path: str):
        """
        Заполнение таблицы данными полученными в запросе к облаку.
        """
        self.ui.tableWidget.setRowCount(0)
        row_position = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(row_position)
        self.ui.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem("..."))
        self.files.update({"...": {"path": path, "isdir": True}})
        for path in files:
            row_position = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row_position)
            self.ui.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(path.get("name")))
            self.files.update({path.get("name"): {"path": path.get("path"), "isdir": path.get("isdir")}})
        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)

    @staticmethod
    def getOpenFilesAndDirs(parent=None, caption='', directory='', filter='', initialFilter='', options=None) -> list:
        """
        Создание окна для выбора файлов или папок для загрузки.
        """
        def updateText():
            selected = []
            for index in view.selectionModel().selectedRows():
                selected.append('"{}"'.format(index.data()))
            lineEdit.setText(' '.join(selected))

        dialog = QtWidgets.QFileDialog(parent, windowTitle=caption)
        dialog.setFileMode(dialog.ExistingFiles)
        if options:
            dialog.setOptions(options)
        dialog.setOption(dialog.DontUseNativeDialog, True)
        if directory:
            dialog.setDirectory(directory)
        if filter:
            dialog.setNameFilter(filter)
            if initialFilter:
                dialog.selectNameFilter(initialFilter)

        dialog.accept = lambda: QtWidgets.QDialog.accept(dialog)

        stackedWidget = dialog.findChild(QtWidgets.QStackedWidget)
        view = stackedWidget.findChild(QtWidgets.QListView)
        view.selectionModel().selectionChanged.connect(updateText)

        lineEdit = dialog.findChild(QtWidgets.QLineEdit)
        dialog.directoryEntered.connect(lambda: lineEdit.setText(''))

        dialog.exec_()
        return dialog.selectedFiles()

    def input_pass(self):
        """
        Диалоговое окно для ввода пароля для шифрования логина и пароля для облака.
        """
        text, ok = QInputDialog.getText(self, 'Ввод пароля', 'Введите пароль:')
        return text if ok else False


class InputDialog(QDialog):
    """
    Создание диалога с двумя полями ввода для логина и пароля облака.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.first = QLineEdit(self)
        self.second = QLineEdit(self)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        layout = QFormLayout(self)
        layout.addRow("Cloud Mail Login", self.first)
        layout.addRow("Cloud Mail Password", self.second)
        layout.addWidget(button_box)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

    def get_inputs(self) -> tuple:
        return self.first.text(), self.second.text()


def cpu() -> (str, bool):
    """
    Получение серийного номера процессора для шифрования, который
    будет использоваться в Windows вместо пароля для шифрования.
    """
    from wmi import WMI
    cp = WMI().Win32_Processor()[0].ProcessorId
    return cp if cp else False


def encrypt_word(word: str, pw: str) -> str:
    """
    Шифрование логина и пароля.
    """
    return encrypt(word, pw)


if __name__ == '__main__':
    """
    Проверка наличия файла с настройками. Если нет, запрашиваем
    логин и пароль, шифруем и сохраняем в файл.
    Проверяем, если ОС Windows используем для шифрования серийный 
    номер процессора. Если получить не удалось, запрашиваем у пользователя
    пароль для шифрования введенных данных для входа в облако.
    Если ОС Linux, запрашиваем у пользователя пароль для шифрования данных
    для входа в облако.
    Авторизация в облаке с полученным серийным номером или введенным паролем.
    Запуск приложения.
    """
    app = QtWidgets.QApplication(argv)
    myapp = MyWin()
    psw = None
    if psys() == "Windows":
        psw = cpu()
        if not psw:
            psw = myapp.input_pass()
            if not psw:
                ext(0)
    elif psys() == "Linux":
        psw = myapp.input_pass()
        if not psw:
            ext(0)
    if not check_setting():
        dialog = InputDialog()
        if dialog.exec():
            login, password = dialog.get_inputs()
            if not login or not password:
                print("Данные для входа в Облако не получены")
                sys.exit(0)
            with open("setting.ini", "w", encoding="utf-8") as file:
                file.write(f'{encrypt_word(login, psw)}\n')
                file.write(f'{encrypt_word(password, psw)}\n')
        else:
            ext(0)
    client = authorize(psw)
    if client:
        myapp.client = client
        myapp.connect_cloud(path="/")
        myapp.show()
        ext(app.exec_())
    else:
        print("Авторизация на удалась. Проверьте файл setting.ini")
