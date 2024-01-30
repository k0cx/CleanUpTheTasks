import hashlib
import json
import platform

from cryptocode import encrypt, decrypt
from pathlib import Path
from webdav3.client import Client  # pip webdavclient3
from webdav3.exceptions import WebDavException  # pip webdavclient3

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from kivymd.app import MDApp
from kivymd.toast.kivytoast.kivytoast import toast
from kivymd.uix.relativelayout import MDRelativeLayout

from data.data_init import data_dir_init

cutt_data_dir = data_dir_init().dir_init()


class SettingsScreen(Screen):
    def on_pre_enter(self):
        sm = MDApp.get_running_app().root
        login = sm.ids.settings_screen.ids.login_field
        password = sm.ids.settings_screen.ids.password_container.ids.password_field
        settings_json = cutt_data_dir / "settings.json"
        try:
            with open(settings_json, "r", encoding="utf-8") as file:
                data = json.load(file)

            key_word = self.generate_key_word()
            login.text = decrypt(data["webdav_login"], key_word)
            password.text = decrypt(data["webdav_password"], key_word)
        except:
            settings_json.touch()

    def generate_key_word(self):
        cpu_inf = str(
            str(platform.system())
            + str(platform.node())
            + str(platform.version())
            + str(platform.processor())
            + str(platform.architecture())
            + str(platform.machine())
        ).replace(" ", "")
        d = hashlib.sha256()
        d.update(cpu_inf.encode("utf-8", errors="ignore"))
        return d.hexdigest()

    def encrypt_word(word: str, key_word: str) -> str:
        return encrypt(key_word)

    def decrypt_word(word: str, key_word: str) -> str:
        return decrypt(word, key_word)

    def crypt_input(self):
        key_word = self.generate_key_word()
        sm = MDApp.get_running_app().root
        login = sm.ids.settings_screen.ids.login_field
        password = sm.ids.settings_screen.ids.password_container.ids.password_field

        data = {
            "webdav_hostname": "https://webdav.cloud.mail.ru",
            "webdav_login": encrypt(login.text, key_word),
            "webdav_password": encrypt(password.text, key_word),
        }
        settings_json = cutt_data_dir / "settings.json"
        with open(settings_json, "w", encoding="utf-8") as file:
            json.dump(data, file)

    def check_client(self):
        settings_json = cutt_data_dir / "settings.json"
        with open(settings_json, "r", encoding="utf-8") as file:
            data = json.load(file)

        key_word = self.generate_key_word()
        decrypt_data = {
            "webdav_login": decrypt(data["webdav_login"], key_word),
            "webdav_password": decrypt(data["webdav_password"], key_word),
        }
        data.update(decrypt_data)

        try:
            client = Client(data)
            # client.verify = False
            client.list()
            toast(text="OK", duration=2)
        except WebDavException as exception:
            print(exception)
            toast(text="FAULT", duration=5)

    def back_action(self):
        sm = MDApp.get_running_app().root
        sm.transition = SlideTransition(direction="right")
        sm.current = "task list screen"


class PasswordField(MDRelativeLayout):
    pass
