from kivy.config import Config

Config.set("graphics", "resizable", True)
Config.set("graphics", "width", "350")
Config.set("graphics", "height", "600")
Config.set("kivy", "exit_on_escape", "0")

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# from kivy.properties import StringProperty

from kivymd.app import MDApp

# from kivymd.uix.screenmanager import MDScreenManager

# from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
# from kivymd.uix.selectioncontrol import MDCheckbox

# from kivymd.uix.textfield import MDTextField

# from datetime import datetime

from assets.task_list_screen import TaskListScreen, ListItemWithCheckbox
from assets.add_task_screen import AddTaskScreen, EditTaskScreen

from assets.database import Database

# Initialize db instance
db = Database()


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

        try:
            completed_tasks, uncomplete_tasks = db.get_tasks()

            if uncomplete_tasks != []:
                for task in uncomplete_tasks:
                    add_task = ListItemWithCheckbox(
                        pk=task[0],
                        text=task[1],
                        secondary_text=task[2],
                    )
                    # self.root.ids.container.add_widget(add_task)
                    self.root.get_screen(
                        name="task list screen"
                    ).ids.container.add_widget(add_task)

            if completed_tasks != []:
                for task in completed_tasks:
                    add_task = ListItemWithCheckbox(
                        pk=task[0],
                        text="[s]" + task[1] + "[/s]",
                        secondary_text=task[2],
                    )
                    add_task.ids.check.active = True
                    # self.root.ids.container.add_widget(add_task)
                    self.root.get_screen(
                        name="task list screen"
                    ).ids.container.add_widget(add_task)
        except Exception as e:
            print(e)
            pass


if __name__ == "__main__":
    MainApp().run()
