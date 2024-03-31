from kivy.config import Config

Config.set("graphics", "resizable", True)
Config.set("graphics", "width", "350")
Config.set("graphics", "height", "600")
Config.set("kivy", "exit_on_escape", "0")
Config.set("kivy", "window_icon", "assets/cutt-icon.png")

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.app import MDApp

from screens.task_list_screen import TaskListScreen, TaskListCreator, EditTaskView

# from screens.edit_task_screen import EditTaskScreen
from screens.settings_screen import SettingsScreen

Builder.load_file("screens/task_list_screen.kv")
Builder.load_file("screens/edit_task_view.kv")
# Builder.load_file("screens/edit_task_screen.kv")
Builder.load_file("screens/settings_screen.kv")


class RootScreenManager(ScreenManager):
    pass


class MainApp(MDApp):
    def build(self):
        # Setting theme
        self.theme_cls.primary_palette = "DeepOrange"
        self.theme_cls.material_style = "M3"
        self.icon = "assets/cutt-icon.png"
        return RootScreenManager()

    def on_start(self):
        TaskListCreator().create_task_list_widget()  # load tasks to widget


if __name__ == "__main__":
    MainApp().run()
