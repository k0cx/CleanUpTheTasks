from kivy.config import Config

Config.set("graphics", "resizable", True)
Config.set("graphics", "width", "350")
Config.set("graphics", "height", "600")
Config.set("kivy", "exit_on_escape", "0")

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

# from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch

# from kivymd.uix.screen import MDScreen
# from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField

from datetime import datetime

from .add_task_screen import AddTaskScreen
from .database import Database

# Initialize db instance
db = Database()

Builder.load_file("assets/task_list_screen.kv")
Builder.load_file("assets/groups_view.kv")
# Builder.load_file("assets/add_task_screen.kv")
# Builder.load_file("assets/edit_task_screen.kv")


class GroupsView(MDBoxLayout):
    pass


class EditTaskScreen(Screen):
    pass


class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    """Custom list item"""

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.pk = pk

    def mark(self, check, the_list_item):
        """mark the task as complete or incomplete"""
        if check.active == True:
            # add strikethrough to the text if the checkbox is active
            the_list_item.text = "[s]" + the_list_item.text + "[/s]"
            db.mark_task_as_complete(the_list_item.pk)
        else:
            the_list_item.text = str(db.mark_task_as_incomplete(the_list_item.pk))

    def delete_item(self, the_list_item):
        """Delete the task"""
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)

    def edit_task(self, the_list_item):
        task_data = db.get_task_data(the_list_item.pk)
        print(task_data)
        edit_task_name = MDTextField(
            # pk=task_data[0],
            text=task_data[2],
            # secondary_text=task_data[2],
        )
        # self.ids.screen_manager.name("edit task screen").ids.edit_container.add_widget(
        #     edit_task_name
        # )


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    """Custom left container"""


class TaskListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_start(self):
        """Load the saved tasks and add them to the MDList widget when the application starts"""

        self.add_widget(MDLabel(text="name_theme", halign="center"))

        try:
            completed_tasks, uncomplete_tasks = db.get_tasks()

            if uncomplete_tasks != []:
                for task in uncomplete_tasks:
                    add_task = ListItemWithCheckbox(
                        pk=task[0],
                        text=task[1],
                        secondary_text=task[2],
                    )
                    self.root.ids.container.add_widget(add_task)

            if completed_tasks != []:
                for task in completed_tasks:
                    add_task = ListItemWithCheckbox(
                        pk=task[0],
                        text="[s]" + task[1] + "[/s]",
                        secondary_text=task[2],
                    )
                    add_task.ids.check.active = True
                    self.root.ids.container.add_widget(add_task)
        except Exception as e:
            print(e)
            pass
