import json
import datetime

from cryptography.fernet import Fernet
from pathlib import Path

from webdav3.client import Client  # pip webdavclient3
from webdav3.exceptions import WebDavException  # pip webdavclient3

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from kivymd.app import MDApp
from kivymd.toast.kivytoast.kivytoast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout

from data.data_init import data_dir_init

cutt_data_dir = data_dir_init().dir_init()
settings_json = cutt_data_dir / "settings.json"


class SettingsView(MDBoxLayout):
    def on_settings_enter(self):
        scrn = MDApp.get_running_app().root.get_screen(name="task list screen")
        host = scrn.ids.settings_view.ids.host_field
        login = scrn.ids.settings_view.ids.login_field
        password = scrn.ids.settings_view.ids.password_container.ids.password_field
        label_connection = scrn.ids.settings_view.ids.label_connection
        label_export = scrn.ids.settings_view.ids.label_export
        label_import = scrn.ids.settings_view.ids.label_import

        if settings_json.exists():
            with open(settings_json, "r", encoding="utf-8") as file:
                data = json.load(file)

            b_word = Fernet(data["client_uid"].encode("utf-8"))
            if data["webdav_login"] == "":
                login.text = ""
            else:
                b_login = data["webdav_login"].encode("utf-8")
                login.text = b_word.decrypt(b_login).decode("utf-8")
            if data["webdav_password"] == "":
                login.text = ""
            else:
                b_password = data["webdav_password"].encode("utf-8")
                password.text = b_word.decrypt(b_password).decode("utf-8")

            host.text = data["webdav_hostname"]
            label_connection.text = data["connection_check"]
            label_export.text = data["last_export"]
            label_import.text = data["last_import"]

        else:
            settings_json.touch()
            data = {
                "client_uid": Fernet.generate_key().decode("utf-8"),
                "webdav_hostname": "https://",
                "webdav_login": "",
                "webdav_password": "",
                "connection_check": "Connection check: \n none",
                "last_export": "Last export: \n never",
                "last_import": "Last import: \n never",
            }
            with open(settings_json, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

    def crypt_input(self):
        scrn = MDApp.get_running_app().root.get_screen(name="task list screen")
        host = scrn.ids.settings_view.ids.host_field
        login = scrn.ids.settings_view.ids.login_field
        password = scrn.ids.settings_view.ids.password_container.ids.password_field
        b_login = login.text.encode("utf-8")
        b_password = password.text.encode("utf-8")

        with open(settings_json, "r", encoding="utf-8") as file:
            data = json.load(file)

        b_word = Fernet(data["client_uid"].encode("utf-8"))

        inp_data = {
            "webdav_hostname": host.text,
            "webdav_login": b_word.encrypt(b_login).decode("utf-8"),
            "webdav_password": b_word.encrypt(b_password).decode("utf-8"),
        }
        data.update(inp_data)

        with open(settings_json, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def check_client(self):
        settings_view = (
            MDApp.get_running_app()
            .root.get_screen(name="task list screen")
            .ids.settings_view
        )
        connection_label = settings_view.ids.label_connection

        with open(settings_json, "r", encoding="utf-8") as file:
            data = json.load(file)

        b_word = Fernet(data["client_uid"].encode("utf-8"))
        b_login = data["webdav_login"].encode("utf-8")
        b_password = data["webdav_password"].encode("utf-8")
        decrypt_data = {
            "webdav_hostname": data["webdav_hostname"],
            "webdav_login": b_word.decrypt(b_login).decode("utf-8"),
            "webdav_password": b_word.decrypt(b_password).decode("utf-8"),
        }

        try:
            client = Client(decrypt_data)
            client.list()
            toast(text="OK", duration=2)
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            connection_label.text = "Connection check: \n" + str(now)
        except WebDavException:
            toast(text="exception", duration=5)
            connection_label.text = "Connection check: \n none"
        finally:
            data["connection_check"] = connection_label.text
            with open(settings_json, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

    def webdav_export(self):
        settings_view = (
            MDApp.get_running_app()
            .root.get_screen(name="task list screen")
            .ids.settings_view
        )
        export_label = settings_view.ids.label_export

        with open(settings_json, "r", encoding="utf-8") as file:
            data = json.load(file)
        b_word = Fernet(data["client_uid"].encode("utf-8"))
        b_login = data["webdav_login"].encode("utf-8")
        b_password = data["webdav_password"].encode("utf-8")
        decrypt_data = {
            "webdav_hostname": data["webdav_hostname"],
            "webdav_login": b_word.decrypt(b_login).decode("utf-8"),
            "webdav_password": b_word.decrypt(b_password).decode("utf-8"),
        }

        try:
            client = Client(decrypt_data)
            if client.check("CUTT") is True:
                client.upload_sync(
                    remote_path="CUTT/todo.db", local_path=cutt_data_dir / "todo.db"
                )
            else:
                client.mkdir("CUTT")
                client.upload_sync(
                    remote_path="CUTT/todo.db", local_path=cutt_data_dir / "todo.db"
                )
            toast(text="OK", duration=2)
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            export_label.text = "Last export: \n" + str(now)
            data["last_export"] = export_label.text
            with open(settings_json, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except WebDavException:
            toast(text="failed", duration=5)

    def webdav_import(self):
        settings_view = (
            MDApp.get_running_app()
            .root.get_screen(name="task list screen")
            .ids.settings_view
        )
        import_label = settings_view.ids.label_import

        with open(settings_json, "r", encoding="utf-8") as file:
            data = json.load(file)
        b_word = Fernet(data["client_uid"].encode("utf-8"))
        b_login = data["webdav_login"].encode("utf-8")
        b_password = data["webdav_password"].encode("utf-8")
        decrypt_data = {
            "webdav_hostname": data["webdav_hostname"],
            "webdav_login": b_word.decrypt(b_login).decode("utf-8"),
            "webdav_password": b_word.decrypt(b_password).decode("utf-8"),
        }

        try:
            client = Client(decrypt_data)
            if client.check("CUTT"):
                client.download_sync(
                    remote_path="CUTT/todo.db", local_path=cutt_data_dir / "todo.db"
                )
                toast(text="OK", duration=2)
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                import_label.text = "Last import: \n" + str(now)
                data["last_import"] = import_label.text
                with open(settings_json, "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4)
            else:
                toast(text="no remote dir", duration=2)
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                import_label.text = "No remote dir! \n" + str(now)
        except WebDavException:
            toast(text="failed", duration=5)


class PasswordField(MDRelativeLayout):
    pass
