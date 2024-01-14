import bcrypt
from pathlib import Path

# from cryptocode import decrypt
from webdav3.client import Client

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from kivymd.app import MDApp
from kivymd.uix.relativelayout import MDRelativeLayout


class SettingsScreen(Screen):
    def back_action(self):
        sm = MDApp.get_running_app().root
        sm.transition = SlideTransition(direction="right")
        sm.current = "task list screen"

    def crypt_input(self):
        sm = MDApp.get_running_app().root
        with open(Path(__file__).parent.resolve() / "settings.ini", "wb") as f:
            f.write(
                bcrypt.hashpw(
                    sm.ids.settings_screen.ids.login_field.text.encode(),
                    bcrypt.gensalt(),
                )
            )
        with open(Path(__file__).parent.resolve() / "settings2.ini", "wb") as f:
            f.write(
                bcrypt.hashpw(
                    sm.ids.settings_screen.ids.password_container.ids.password_field.text.encode(),
                    bcrypt.gensalt(),
                )
            )

    def check_crypt(self):
        sm = MDApp.get_running_app().root
        with open(Path(__file__).parent.resolve() / "settings.ini", "rb") as f:
            b_login = f.read()
            print(
                bcrypt.checkpw(
                    sm.ids.settings_screen.ids.login_field.text.encode(),
                    bcrypt.gensalt(),
                )
            )
        with open(Path(__file__).parent.resolve() / "settings2.ini", "rb") as f:
            f.read(
                bcrypt.hashpw(
                    sm.ids.settings_screen.ids.password_container.ids.password_field.text.encode(),
                    bcrypt.gensalt(),
                )
            )

    def check_client(self):
        data = {
            "webdav_hostname": "https://webdav.cloud.mail.ru",
            "webdav_login": b_login,
            "webdav_password": b_password,  # ubuntu
        }
        client = Client(data)

        my_files = client.list()
        print(my_files)


class PasswordField(MDRelativeLayout):
    pass
