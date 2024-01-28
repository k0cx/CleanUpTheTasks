import platform

from pathlib import Path
from kivy.config import Config

Config.set("graphics", "resizable", True)
Config.set("graphics", "width", "350")
Config.set("graphics", "height", "600")
Config.set("kivy", "exit_on_escape", "0")

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.app import MDApp

from screens.task_list_screen import TaskListScreen, TaskListCreator
from screens.edit_task_screen import EditTaskScreen
from screens.settings_screen import SettingsScreen

# if platform == "android":
#     from android.permissions import request_permissions, Permission

#     request_permissions(
#         [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE]
#     )

Builder.load_file("screens/task_list_screen.kv")
Builder.load_file("screens/groups_view.kv")
Builder.load_file("screens/edit_task_screen.kv")
Builder.load_file("screens/settings_screen.kv")


class RootScreenManager(ScreenManager):
    pass


class MainApp(MDApp):
    def build(self, *args):
        # Setting theme
        self.theme_cls.primary_palette = "DeepOrange"
        self.theme_cls.material_style = "M3"
        from android.permissions import request_permissions, Permission

        request_permissions(
            [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE]
        )
        # from android.storage import primary_external_storage_path

        # global primary_ext_storage
        # primary_ext_storage = primary_external_storage_path()
        # primary_ext_storage = Path.home()
        return RootScreenManager()

    def on_start(self):
        cutt_data_dir = Path.home() / "Clean up the tasks"
        if cutt_data_dir.exists() == False:
            cutt_data_dir.mkdir()

        TaskListCreator().create_task_list_widget()  # load tasks to widget


if __name__ == "__main__":
    MainApp().run()
