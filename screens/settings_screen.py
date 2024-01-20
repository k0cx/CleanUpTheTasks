# import bcrypt
from pathlib import Path

from cpuinfo import get_cpu_info  # py-cpuinfo
import hashlib
from cryptocode import encrypt, decrypt
from webdav3.client import Client  # webdavclient3

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from kivymd.app import MDApp
from kivymd.uix.relativelayout import MDRelativeLayout


class SettingsScreen(Screen):
    def generate_key_word(self):
        # cpu_info = cpuinfo.get_cpu_info()

        cpu_inf = (
            "%s%s%s%s"
            % (
                get_cpu_info()["model"],
                get_cpu_info()["family"],
                "".join(get_cpu_info()["flags"]),
                get_cpu_info()["arch"],
            )
        ).replace(" ", "")

        # print(cpu_inf)
        d = hashlib.sha1()
        d.update(cpu_inf.encode("utf-8", errors="ignore"))
        # with open(
        #     Path(__file__).parent.resolve() / "settings2.ini", "w", encoding="utf-8"
        # ) as file:
        #     file.write(d.hexdigest())
        return d.hexdigest()

    def encrypt_word(word: str, key_word: str) -> str:
        return encrypt(key_word)

    def decrypt_word(word: str, key_word: str) -> str:
        return decrypt(word, key_word)

    def crypt_input(self):
        sm = MDApp.get_running_app().root
        # key_word = "The best password for Clean_up_the_Tasks"
        login = sm.ids.settings_screen.ids.login_field.text
        password = sm.ids.settings_screen.ids.password_container.ids.password_field.text
        key_word = self.generate_key_word()
        settings_ini = Path(__file__).parents[1] / "data/settings.ini"

        with open(settings_ini, "w", encoding="utf-8") as file:
            file.write(f"{encrypt(login, key_word)}\n")
            file.write(f"{encrypt(password, key_word)}\n")

    def check_client(self):
        settings_ini = Path(__file__).parents[1] / "data/settings.ini"
        credentials = [
            x.strip() for x in open(settings_ini, "r", encoding="utf-8") if x.strip()
        ]
        key_word = self.generate_key_word()
        login = decrypt(credentials[0], key_word)
        password = decrypt(credentials[1], key_word)
        data = {
            "webdav_hostname": "https://webdav.cloud.mail.ru",
            "webdav_login": login,
            "webdav_password": password,  # ubuntu
        }
        client = Client(data)

        my_files = client.list()
        print(my_files)

    def back_action(self):
        sm = MDApp.get_running_app().root
        sm.transition = SlideTransition(direction="right")
        sm.current = "task list screen"


class PasswordField(MDRelativeLayout):
    pass
