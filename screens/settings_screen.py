import json

from cryptography.fernet import Fernet
from pathlib import Path

from webdav3.client import Client  # pip webdavclient3
from webdav3.exceptions import WebDavException  # pip webdavclient3

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from kivymd.app import MDApp
from kivymd.toast.kivytoast.kivytoast import toast
from kivymd.uix.relativelayout import MDRelativeLayout

from data.data_init import data_dir_init

cutt_data_dir = data_dir_init().dir_init()
settings_json = cutt_data_dir / "settings.json"


class SettingsScreen(Screen):
    def on_pre_enter(self):
        sm = MDApp.get_running_app().root
        login = sm.ids.settings_screen.ids.login_field
        password = sm.ids.settings_screen.ids.password_container.ids.password_field
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
        else:
            settings_json.touch()
            data = {
                "client_uid": Fernet.generate_key().decode("utf-8"),
                "webdav_hostname": "https://webdav.cloud.mail.ru",
                "webdav_login": "",
                "webdav_password": "",
            }
            with open(settings_json, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

    def crypt_input(self):
        sm = MDApp.get_running_app().root
        login = sm.ids.settings_screen.ids.login_field
        password = sm.ids.settings_screen.ids.password_container.ids.password_field
        b_login = login.text.encode("utf-8")
        b_password = password.text.encode("utf-8")

        with open(settings_json, "r", encoding="utf-8") as file:
            data = json.load(file)

        b_word = Fernet(data["client_uid"].encode("utf-8"))

        inp_data = {
            "webdav_login": b_word.encrypt(b_login).decode("utf-8"),
            "webdav_password": b_word.encrypt(b_password).decode("utf-8"),
        }
        data.update(inp_data)

        with open(settings_json, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def check_client(self):
        try:
            with open(settings_json, "r", encoding="utf-8") as file:
                data = json.load(file)

            b_word = Fernet(data["client_uid"].encode("utf-8"))
            b_login = data["webdav_login"].encode("utf-8")
            b_password = data["webdav_password"].encode("utf-8")
            decrypt_data = {
                "webdav_login": b_word.decrypt(b_login).decode("utf-8"),
                "webdav_password": b_word.decrypt(b_password).decode("utf-8"),
            }
            data.pop("client_uid", None)
            data.update(decrypt_data)

            try:
                client = Client(data)
                # client.verify = False
                client.list()
                toast(text="OK", duration=2)
            except WebDavException as exception:
                print(exception)
                toast(text=exception, duration=5)
        except:
            toast(text="save login and password first", duration=3)

    def back_action(self):
        sm = MDApp.get_running_app().root
        sm.transition = SlideTransition(direction="right")
        sm.current = "task list screen"


class PasswordField(MDRelativeLayout):
    pass
