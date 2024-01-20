from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.app import MDApp

from assets.task_list_screen import TaskListScreen, TaskListCreator

# from assets.task_list_screen import *
from assets.edit_task_screen import *
from assets.settings_screen import *
from assets.database import Database

Config.set("graphics", "resizable", True)
Config.set("graphics", "width", "350")
Config.set("graphics", "height", "600")
Config.set("kivy", "exit_on_escape", "0")

Builder.load_file("assets/task_list_screen.kv")
Builder.load_file("assets/groups_view.kv")
Builder.load_file("assets/edit_task_screen.kv")
Builder.load_file("assets/settings_screen.kv")


class RootScreenManager(ScreenManager):
    pass


class MainApp(MDApp):
    def build(self, *args):
        # Setting theme
        self.theme_cls.primary_palette = "DeepOrange"
        self.theme_cls.material_style = "M3"
        return RootScreenManager()

    def on_start(self):
        """Load the saved tasks and add them to the MDList widget when the application starts"""

        TaskListCreator().create_task_list_widget()


if __name__ == "__main__":
    MainApp().run()
