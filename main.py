from kivy.config import Config

Config.set("graphics", "resizable", True)
Config.set("graphics", "width", "350")
Config.set("graphics", "height", "600")
Config.set("kivy", "exit_on_escape", "0")

from kivy.lang import Builder

# from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

# from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
# from kivymd.uix.selectioncontrol import MDCheckbox
# from kivymd.uix.textfield import MDTextField

# from datetime import datetime

from assets.task_list_screen import TaskListScreen
from assets.add_task_screen import AddTaskScreen

# from assets.database import Database

# Initialize db instance
# db = Database()


class RootScreenManager(MDScreenManager):
    pass


class MainApp(MDApp):
    def build(self, *args):
        # Setting theme
        self.theme_cls.primary_palette = "DeepOrange"
        self.theme_cls.material_style = "M3"
        return RootScreenManager()


if __name__ == "__main__":
    MainApp().run()
