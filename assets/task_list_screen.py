from kivy.config import Config

Config.set("graphics", "resizable", True)
Config.set("graphics", "width", "350")
Config.set("graphics", "height", "600")
Config.set("kivy", "exit_on_escape", "0")

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch

# from kivymd.uix.screen import MDScreen
# from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField

from datetime import datetime

from assets.database import Database

# Initialize db instance
db = Database()


class GroupsView(MDBoxLayout):
    pass


class TaskListScreen(Screen):
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
        edit_task_ids = MDApp.get_running_app().root.ids.edit_task_screen.ids
        edit_task_ids["task_text"].text = task_data[2]
        edit_task_ids["date_text"].text = task_data[3]


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    """Custom left container"""
